from django.shortcuts import get_object_or_404

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from app_users.models import User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        request_user = "A"
        match_user = "B"
        self.room_group_name = f"{request_user}_to_{match_user}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sending_user = text_data_json["sending_user"]
        sending_user_pk = int(text_data_json["sending_user_pk"])
        if int(sending_user_pk) > 0:
            current_user = get_object_or_404(User, pk=int(sending_user_pk))
            print(current_user)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sending_user": sending_user,
                "sending_user_pk": sending_user_pk,
            },
        )

    def chat_message(self, event):
        # breakpoint()
        message = event["message"]
        sending_user = event["sending_user"]
        sending_user_pk = int(event["sending_user_pk"])
        if int(sending_user_pk) > 0:
            current_user = get_object_or_404(User, pk=sending_user_pk)
            print(current_user)

        self.send(
            text_data=json.dumps(
                {
                    "type": "chat",
                    "message": message,
                    "sending_user": sending_user,
                    "sending_user_pk": sending_user_pk,
                }
            )
        )
