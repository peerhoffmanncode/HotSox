from rest_framework import serializers
from app_users.models import (
    User,
    UserMatch,
    UserProfilePicture,
    Sock,
    SockLike,
    SockProfilePicture,
    MessageMail,
    MessageChat,
)


class SockLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SockLike
        exclude = ["sock"]


class SockProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SockProfilePicture
        exclude = ["sock"]


class SockSerializer(serializers.ModelSerializer):
    sock_likes = SockLikeSerializer(many=True)
    profile_picture = SockProfilePictureSerializer(many=True)

    class Meta:
        model = Sock
        exclude = ["user"]


class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageMail
        exclude = ["user"]


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageChat
        exclude = ["user"]


class UserMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMatch
        fields = "__all__"


class UserProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfilePicture
        exclude = ["user"]


class UserSerializer(serializers.ModelSerializer):
    user_match = UserMatchSerializer(many=True)
    profile_picture = UserProfilePicSerializer(many=True)
    sock = SockSerializer(many=True)
    mail = MailSerializer(many=True)
    chat_sending = ChatSerializer(many=True)

    class Meta:
        model = User
        exclude = ["password", "groups", "user_permissions"]
