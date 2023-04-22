from rest_framework import serializers
from datetime import date
from django.core.exceptions import ValidationError
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

# import default Django password hashing function
from django.contrib.auth.hashers import make_password


def validate_age(value):
    difference = date.today() - value
    if round(difference.days / 365.2425, 2) < 18:
        raise ValidationError("You must be at least 18 years old", code="invalid")
    return value


class SockLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SockLike
        exclude = ["sock"]


class SockProfilePictureSerializer(serializers.ModelSerializer):
    # this is needed to show a upload file dialog!
    profile_picture = serializers.FileField()

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


class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class ChatSerializer(serializers.ModelSerializer):
    other = UserChatSerializer()

    class Meta:
        model = MessageChat
        exclude = ["user"]


class ChatSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageChat
        fields = ["message"]


class UserMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMatch
        fields = "__all__"


class UserProfilePicSerializer(serializers.ModelSerializer):
    # this is needed to show a upload file dialog!
    profile_picture = serializers.FileField()

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


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "groups",
            "user_permissions",
            "is_staff",
            "is_superuser",
            "is_active",
            "last_login",
            "date_joined",
            "location_longitude",
            "location_latitude",
        ]

    def validate_info_birthday(self, value):
        return validate_age(value)

    # enforce password hashing
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super(UserCreateSerializer, self).create(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "id",
            "password",
            "groups",
            "user_permissions",
            "is_staff",
            "is_superuser",
            "is_active",
            "last_login",
            "date_joined",
            "location_longitude",
            "location_latitude",
        ]

    def validate_info_birthday(self, value):
        return validate_age(value)

    # enforce password hashing
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super(UserUpdateSerializer, self).create(validated_data)
