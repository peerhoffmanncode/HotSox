from django.shortcuts import render, redirect
from django.urls import reverse
from app_users.models import User, UserMatch, MessageChat
from django.db.models import Q

from django.utils import timezone


# TODO: rewrite as classbased view
def chat_with_match(request, matched_user_name):
    """Main view to initiate a new chat conversation
    Gather the User, matched user, and all the chats that have been done
    get a chatroom UUID
    """

    # define a url to redirect to if an invalid record is detected
    error_url = reverse("app_users:user-matches")

    # get the other user object from the url argument
    try:
        matched_user = User.objects.get(username=matched_user_name)
    except User.DoesNotExist:
        # if no valid matched user was found we redirect to error url
        return redirect(error_url)

    # get the UserMatch object to obtain the chatroom UUID
    try:
        user_match_object = UserMatch.objects.get(
            Q(user=request.user, other=matched_user)
            | Q(user=matched_user, other=request.user)
        )
        chatroom_uuid = str(user_match_object.chatroom_uuid)
        request.session["chatroom_uuid"] = chatroom_uuid
    except UserMatch.DoesNotExist:
        # if no valid match was found we redirect to error url
        return redirect(error_url)

    # get all chats send my the current user (to matched user)
    all_chats = MessageChat.objects.filter(
        Q(user=request.user, other=matched_user)
        | Q(user=matched_user, other=request.user)
    ).order_by("sent_date")

    # every chat message that was sent by the matched users
    # will be marked as seen since it is now displayed to the user
    # every message that was stored above the max count will be deleted
    max_allowes_stored_chats = 300
    max_allowes_stored_chats_count = 0
    for chat in all_chats:
        if max_allowes_stored_chats_count >= max_allowes_stored_chats:
            chat.delete()
        else:
            if chat.other == request.user:
                if not chat.seen_date:
                    chat.seen_date = timezone.now()
                    chat.save()
        max_allowes_stored_chats_count += 1

    context = {
        "sending_user": request.user,
        "receiving_user": matched_user,
        "all_chats": all_chats[:max_allowes_stored_chats],
        "chatroom_UUID": chatroom_uuid,
    }
    return render(request, "chat/chat_lobby.html", context)
