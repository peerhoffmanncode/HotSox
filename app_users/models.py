import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date, timedelta

# CHOICES FOR USER
from .models_choices import (
    GENDER_CHOICES,
    COLOR_CHOICES,
    FABRIC_CHOICES,
    FABRIC_THICKNESS_CHOICES,
    BRAND_CHOICES,
    TYPE_CHOICES,
    SIZE_CHOICES,
    CONDITION_CHOICES,
    ENVIRONMENT_CHOICES,
)


class User(AbstractUser):
    # fields we inherit from AbstractUser:
    # username, password,password_conf,email,first_name,last_name, joining_date, last_login, is_staff, is_active, is_superuser

    info_about = models.TextField(help_text="Insert your story in here.", blank=True)
    info_birthday = models.DateField(default=timezone.now, blank=False)
    info_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=False)
    # info_gender_interest = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=False)
    location_city = models.CharField(
        help_text="Where do you live?", max_length=255, blank=False
    )
    location_latitude = models.FloatField(blank=True, null=True)
    location_longitude = models.FloatField(blank=True, null=True)
    social_instagram = models.URLField(
        help_text="Url to your Instagram profile.",
        max_length=255,
        blank=True,
        null=True,
    )
    social_facebook = models.URLField(
        help_text="Url to your Facebook profile.", max_length=255, blank=True, null=True
    )
    social_twitter = models.URLField(
        help_text="Url to your Twitter profile.", max_length=255, blank=True, null=True
    )
    social_spotify = models.URLField(
        help_text="Url to your Spotify profile.", max_length=255, blank=True, null=True
    )

    def __str__(self) -> str:
        return f"<User {self.first_name.title()} {self.last_name.title()} -> [{self.username}]>"

    def is_18_years(self) -> bool:
        """function the check if a user is older than 18 years"""
        difference = date.today() - self.info_birthday
        # Check if the difference is equal to or greater than 18 years(including leap)
        if round(difference.days / 365.2425, 2) >= 18:
            return True
        else:
            return False

    def to_json(self) -> dict:
        """Function to represent the model as a json dictionary
        !Important: update if changes on the model are made!"""
        return {
            "pk": self.pk,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "info_birthday": self.info_birthday,
            "last_login": self.last_login,
            "date_joined": self.date_joined,
            "is_active": self.is_active,
        }


class UserProfilePicture(models.Model):
    # User.profile_picture.user.pk = User.pk  | himself
    user = models.ForeignKey(
        User, related_name="profile_picture", on_delete=models.CASCADE
    )
    url = models.URLField(max_length=255, blank=False)

    def __str__(self) -> str:
        return f"<UserProfilePicture from {self.user} {self.url}>"


class UserMatch(models.Model):
    # User.him.user.pk = User.pk  | himself
    # User.matched.other.objects.all() = all Other user !
    user = models.ForeignKey(User, related_name="him", on_delete=models.CASCADE)
    other = models.ForeignKey(User, related_name="matched", on_delete=models.CASCADE)


class Sock(models.Model):
    # User.sock.user.pk = User.pk  | himself
    user = models.ForeignKey(User, related_name="sock", on_delete=models.CASCADE)
    info_joining_date = models.DateField(auto_now_add=True, blank=False)

    info_name = (
        models.CharField(
            max_length=255, help_text="What is the socks name?", blank=False
        ),
    )
    info_about = models.TextField(help_text="Insert sock's story in here.", blank=True)
    info_color = models.CharField(
        max_length=10,
        help_text="Select dominant color.",
        choices=COLOR_CHOICES,
        blank=False,
    )
    info_fabric = models.CharField(
        max_length=20,
        help_text="Select main fabric",
        choices=FABRIC_CHOICES,
        blank=False,
    )
    info_fabric_thickness = models.CharField(
        max_length=20,
        help_text="Select main fabric",
        choices=FABRIC_THICKNESS_CHOICES,
        blank=False,
    )
    info_brand = models.CharField(
        max_length=30, help_text="Select the brand.", choices=BRAND_CHOICES, blank=False
    )
    info_type = models.CharField(
        max_length=20, help_text="Select the type.", choices=TYPE_CHOICES, blank=False
    )
    info_size = models.CharField(
        max_length=20, help_text="Select the size.", choices=SIZE_CHOICES, blank=False
    )
    info_age = models.IntegerField(help_text="How old is the sock?", blank=False)
    info_separation_date = models.DateField(
        help_text="Lonely since?", default=timezone.now, blank=False
    )
    info_condition = models.CharField(
        max_length=50,
        help_text="Select the condition of the sock.",
        choices=CONDITION_CHOICES,
        blank=False,
    )
    info_holes = models.IntegerField(
        help_text="How many holes has the sock?", blank=False
    )
    info_kilometers = models.IntegerField(
        help_text="How many kilometers has the sock walked?", blank=False
    )
    info_inoutdoor = models.CharField(
        max_length=20,
        help_text="Select the main environment of the sock.",
        choices=ENVIRONMENT_CHOICES,
        blank=False,
    )
    info_washed = models.IntegerField(
        help_text="How often washed per month?", blank=False
    )
    info_special = models.CharField(
        max_length=250,
        help_text="Description of a special interest of the sock.",
        blank=False,
    )

    def __str__(self) -> str:
        return f"<Sock {self.info_name.title()}>"


class SockProfilePicture(models.Model):
    # Sock.profile_picture.sock.pk = Sock.pk  | sock himself
    sock = models.ForeignKey(
        Sock, related_name="profile_picture", on_delete=models.CASCADE
    )
    url = models.URLField(max_length=255, blank=False)

    def __str__(self) -> str:
        return f"<SockProfilePicture from {self.sock} {self.url}>"


class SockLike(models.Model):
    # Sock.me.sock.pk = Sock.pk  | sock himself
    # Sock.like.other.objects.all() = socks i like
    # Sock.dislike.other.objects.all() = socks i don't like
    sock = models.ForeignKey(
        Sock, related_name="me", on_delete=models.CASCADE, blank=False
    )
    like = models.ForeignKey(
        Sock, related_name="like", on_delete=models.CASCADE, blank=True, null=True
    )
    dislike = models.ForeignKey(
        Sock, related_name="dislike", on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self) -> str:
        return f"<SockLike for {self.sock}>"


class MessageMail(models.Model):
    # User.mail.user.pk = User.pk  | user himself
    user = models.ForeignKey(User, related_name="mail", on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=False)
    sent_date = models.DateField(auto_now_add=True, blank=False)

    def __str__(self) -> str:
        return f"<Mail from {self.user} Subject: {self.subject} @{self.sent_date}>"


class MessageChat(models.Model):
    # User.chat_sending.user.pk = User.pk  | user himself
    # User.chat_receiving.other.objects.all() = user send to !
    user = models.ForeignKey(
        User, related_name="chat_sending", on_delete=models.CASCADE
    )
    other = models.ForeignKey(
        User, related_name="chat_receiving", on_delete=models.CASCADE
    )
    subject = models.CharField(max_length=255, blank=False)
    sent_date = models.DateField(auto_now_add=True, blank=False)
    seen_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return f"<Cat from {self.user} to {self.other} Subject: {self.subject} @{self.sent_date}>"
