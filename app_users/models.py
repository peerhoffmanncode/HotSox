import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date, timedelta

# from django.conf import settings


class User(AbstractUser):
    birthday = models.DateField(default=timezone.now, blank=False)
    SEX_CHOICES = (("female", "Female"), ("male", "Male"), ("divers", "Divers"))
    user_sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=False)
    interested_sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=False)

    def __str__(self) -> str:
        return f"[{self.username}] {self.first_name} {self.last_name}, {str(self.user_sex).capitalize()}"

    def is_18_years(self) -> bool:
        """function the check if a user is older than 18 years"""
        difference = date.today() - self.birthday
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
            "birthday": self.birthday,
            "user_sex": self.user_sex,
            "interested_sex": self.interested_sex,
            "last_login": self.last_login,
            "date_joined": self.date_joined,
            "is_active": self.is_active,
        }
