from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError

from datetime import date
from .models import User


def validate_age(form):
    """function the check if a user is older than 18 years"""

    if isinstance(form, date):
        # handle case where form = birhtday
        difference = date.today() - form
    else:
        # handle case where form = form object
        difference = date.today() - form.cleaned_data["birthday"]

    # Check if the difference is equal to or greater than 18 years(including leap)
    if round(difference.days / 365.2425, 2) < 18:
        raise ValidationError("You must be at least 18 years old", code="invalid")


class UserSignUpForm(UserCreationForm):
    class Meta:
        model = User
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

    def clean(self):
        # Call the custom validator function
        validate_age(self)


class UserEditForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "format": "%d-%m-%Y"}),
    )
    SEX_CHOICES = (("female", "Female"), ("male", "Male"), ("divers", "Divers"))
    user_sex = forms.ChoiceField(choices=SEX_CHOICES)
    interested_sex = forms.ChoiceField(choices=SEX_CHOICES)

    def clean(self):
        # Call the custom validator function
        validate_age(self)
