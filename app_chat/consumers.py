import json
from django.utils import timezone
from django.shortcuts import get_object_or_404

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from app_users.models import User, MessageChat


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        """function to extablish a chat room and connection to the frontend"""

        # obtain the chatroom uuid from the session of the current user!
        chatroom_uuid = self.scope["session"].get("chatroom_uuid", None)
        # set the room_group_name of channels to the correct uuid
        if chatroom_uuid:
            self.room_group_name = chatroom_uuid
        else:
            self.room_group_name = "UNDEFINED"
            raise Exception("No chatroom_uuid defined! This is really bad!")

        # initial the connection
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        # Accepts incoming socket request from the frontend
        self.accept()

    def receive(self, text_data):
        """function to receive chat messages from the room_group_name"""

        # load the json that was send by the frontend JS
        serialized_data_from_chat_frontend = json.loads(text_data)

        was_seen = serialized_data_from_chat_frontend.get("was_seen", None)
        message_pk = serialized_data_from_chat_frontend.get("message_pk", None)
        message = serialized_data_from_chat_frontend.get("message", None)
        sending_user_pk = serialized_data_from_chat_frontend.get(
            "sending_user_pk", None
        )
        sending_user_name = serialized_data_from_chat_frontend.get("sending_user", None)
        receiving_user_pk = serialized_data_from_chat_frontend.get(
            "receiving_user_pk", None
        )
        receiving_user_name = serialized_data_from_chat_frontend.get(
            "receiving_user", None
        )

        # get actual user objects from the database
        if sending_user_pk != "None":
            current_user = get_object_or_404(
                User, pk=sending_user_pk, username=sending_user_name
            )
        if receiving_user_pk != "None":
            matched_user = get_object_or_404(
                User, pk=receiving_user_pk, username=receiving_user_name
            )

        # check if the receiving user has drawn the message
        if was_seen and message_pk:
            # check if data is valid!
            try:
                # get the correct message for the database
                chat_object = MessageChat.objects.filter(pk=message_pk, message=message)
                if chat_object:
                    # get only the first object! Can be multiple because of asyncIO behavior!
                    chat_object = chat_object[0]
                    # check if current user is the receiving user!
                    if self.scope["user"] == chat_object.other:
                        # update the chat message with seen date!
                        chat_object.seen_date = timezone.now()
                        chat_object.save()
                return
            # invalid message!
            except MessageChat.DoesNotExist:
                return
        else:
            # add the key "type" to the serialized data
            serialized_data_from_chat_frontend["type"] = "chat_message"

            # send the serialized data to the frontend
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, serialized_data_from_chat_frontend
            )

    def chat_message(self, event):
        """function to send chat message to the room_group_name"""

        # init user vars
        current_user = matched_user = None

        # get actual user objects from the database
        if event["sending_user_pk"] != "None":
            current_user = get_object_or_404(
                User, pk=event["sending_user_pk"], username=event["sending_user"]
            )
        if event["receiving_user_pk"] != "None":
            matched_user = get_object_or_404(
                User, pk=event["receiving_user_pk"], username=event["receiving_user"]
            )

        # store message in the database
        message_sent_date = message_sent_time = None
        message_seen_date = message_seen_time = None
        chat_object = None

        # check if valid user where found
        if current_user and matched_user:

            # get last send message
            chat_object = MessageChat.objects.filter(
                user=current_user, other=matched_user, message=event["message"]
            ).last()

            # check if last message is exact same message as current one!
            if (
                chat_object
                and chat_object.user == current_user
                and chat_object.other == matched_user
                and chat_object.message == event.get("message", None)
            ):
                # only allow duplicate if within 1 second!
                if timezone.now().strftime("%H%M%S") > chat_object.sent_date.strftime(
                    "%H%M%S"
                ):
                    # create new message in database!
                    chat_object = MessageChat.objects.create(
                        user=current_user, other=matched_user, message=event["message"]
                    )
            else:
                # create new message in database!
                chat_object = MessageChat.objects.create(
                    user=current_user, other=matched_user, message=event["message"]
                )

            message_sent_date = str(chat_object.sent_date.date())
            message_sent_time = str(chat_object.sent_date.time().strftime("%H:%M:%S"))
            if message_seen_date:
                message_seen_date = str(chat_object.seen_date.date())
                message_seen_time = str(
                    chat_object.seen_date.time().strftime("%H:%M:%S")
                )

            print(chat_object.pk, chat_object)

        # serialize data and send to the room_group_name
        self.send(
            text_data=json.dumps(
                {
                    "type": "chat",
                    "message_pk": chat_object.pk if chat_object else None,
                    "message": event["message"],
                    "message_sent_date": message_sent_date,
                    "message_sent_time": message_sent_time,
                    "message_seen_date": message_seen_date,
                    "message_seen_time": message_seen_time,
                    "sending_user_pk": event["sending_user_pk"],
                    "sending_user": event["sending_user"],
                    "receiving_user_pk": event["receiving_user_pk"],
                    "receiving_user": event["receiving_user"],
                }
            )
        )
