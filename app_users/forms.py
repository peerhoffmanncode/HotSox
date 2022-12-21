from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import HotSoxUserModel


class UserSignUpForm(UserCreationForm):
    class Meta:
        model = HotSoxUserModel
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "birthday",
            "user_sex",
            "interested_sex",
        ]

        labels = {
            "username": "Your username",
            "email": "Your email address",
            "first_name": "Your first name",
            "last_name": "Your last name",
            "birthday": "Your birthday",
            "user_sex": "Your sex",
            "interested_sex": "What are you looking for",
        }
        widgets = {
            "birthday": forms.DateInput(attrs={"type": "date", "format": "%d-%m-%Y"}),
        }


class UserEditForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "format": "%d-%m-%Y"})
    )
    SEX_CHOICES = (("female", "Female"), ("male", "Male"), ("divers", "Divers"))
    user_sex = forms.ChoiceField(choices=SEX_CHOICES)
    interested_sex = forms.ChoiceField(choices=SEX_CHOICES)
