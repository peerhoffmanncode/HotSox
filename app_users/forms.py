from django.forms import ModelForm, DateInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ValidationError

from datetime import date
from .models import User, UserProfilePicture, Sock, SockProfilePicture


def validate_age(form):
    """function the check if a user is older than 18 years"""

    if isinstance(form, date):
        # handle case where form = birthday
        difference = date.today() - form
    else:
        # handle case where form = form object
        difference = date.today() - form.cleaned_data["info_birthday"]

    # Check if the difference is equal to or greater than 18 years(including leap)
    if round(difference.days / 365.2425, 2) < 18:
        # self.add_error('date_of_birth', 'Enter a valid date of birth')
        raise ValidationError("You must be at least 18 years old", code="invalid")


class UserSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"
        exclude = [
            "password",
            "date_joined",
            "last_login",
            "is_staff",
            "is_active",
            "is_superuser",
            "groups",
            "user_permissions",
            "location_latitude",
            "location_longitude",
        ]

        labels = {
            "username": "Your username",
            "email": "Your email address",
            "first_name": "Your first name",
            "last_name": "Your last name",
            "info_birthday": "Your birthday",
            "info_gender": "Your gender",
            "location_city": "Where do you live?",
            "social_instagram": "Url to your instagram account",
            "social_facebook": "Url to your facebook account",
            "social_twitter": "Url to your twitter account",
            "social_spotify": "Url to your spotify account",
        }
        widgets = {
            "info_birthday": DateInput(attrs={"type": "date", "format": "%d-%m-%Y"}),
        }

    def clean(self):
        # Call the custom validator function
        validate_age(self)


class UserProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = "__all__"
        exclude = [
            "password",
            "password2",
            "date_joined",
            "last_login",
            "is_staff",
            "is_active",
            "is_superuser",
            "groups",
            "user_permissions",
            "location_latitude",
            "location_longitude",
        ]

        labels = {
            "username": "Your username",
            "email": "Your email address",
            "first_name": "Your first name",
            "last_name": "Your last name",
            "info_birthday": "Your birthday",
            "info_gender": "Your gender",
            "location_city": "Where do you live?",
            "social_instagram": "Url to your instagram account",
            "social_facebook": "Url to your facebook account",
            "social_twitter": "Url to your twitter account",
            "social_spotify": "Url to your spotify account",
        }
        widgets = {
            "info_birthday": DateInput(attrs={"type": "date", "format": "%d-%m-%Y"}),
        }

    def clean(self):
        # Call the custom validator function
        validate_age(self)


class UserProfilePictureForm(ModelForm):
    class Meta:
        model = UserProfilePicture
        fields = "__all__"
        exclude = ["user"]


class SockProfileForm(ModelForm):
    class Meta:
        model = Sock
        fields = "__all__"
        exclude = ["user", "info_joining_date"]

        widgets = {
            "info_separation_date": DateInput(
                attrs={"type": "date", "format": "%d-%m-%Y"}
            ),
        }


class SockProfilePictureForm(ModelForm):
    class Meta:
        model = SockProfilePicture
        fields = "__all__"
        exclude = ["sock"]
