from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, DateInput, URLInput, CheckboxInput, TextInput
from django.forms import ValidationError

from datetime import date
from .models import User, UserProfilePicture, Sock, SockProfilePicture
from .forms_widgets import RangeInput, SwitchCheckboxInput


def validate_age(form):
    """function to check if a user is older than 18 years"""

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


def validate_username(data):
    """function to check if a username is already taken"""

    if isinstance(data, str):
        username = data
    else:
        # handle case where form = form object
        username = data.cleaned_data["username"]
        # check if a user object is present
        if data.instance:
            # check if username is unchanged
            if data.instance.username == username:
                return

    try:
        problematic_username = User.objects.get(username=username)
        raise ValidationError("This username has already been taken!", code="invalid")
    except User.DoesNotExist:
        return


def validate_email(data):
    """function to check if a username is already taken"""

    if isinstance(data, str):
        email = data
    else:
        # handle case where form = form object
        email = data.cleaned_data["email"]
        # check if a user object is present
        if data.instance:
            # check if email is unchanged
            if data.instance.email == email:
                return

    try:
        problematic_email = User.objects.get(email=email)
        raise ValidationError("This email is already in use!", code="invalid")
    except User.DoesNotExist:
        return


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
            "info_about": "Tell your story",
            "info_birthday": "Your birthday",
            "info_gender": "Your gender",
            "location_city": "Where do you live?",
            "notification": "Do you like to get notifications?",
            "social_instagram": "Url to your instagram account",
            "social_facebook": "Url to your facebook account",
            "social_twitter": "Url to your twitter account",
            "social_spotify": "Url to your spotify account",
        }
        widgets = {
            "info_birthday": DateInput(attrs={"type": "date", "format": "%d-%m-%Y"}),
            "social_instagram": URLInput(),
            "social_facebook": URLInput(),
            "social_twitter": URLInput(),
            "social_spotify": URLInput(),
        }

    def clean(self):
        # Call the custom validator function
        validate_age(self)
        validate_username(self)
        validate_email(self)


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
            "info_about": "Tell your story",
            "info_birthday": "Your birthday",
            "info_gender": "Your gender",
            "location_city": "Where do you live?",
            "notification": "Do you like to get notifications?",
            "social_instagram": "Url to your instagram account",
            "social_facebook": "Url to your facebook account",
            "social_twitter": "Url to your twitter account",
            "social_spotify": "Url to your spotify account",
        }
        widgets = {
            "notification": TextInput(
                attrs={
                    "type": "Checkbox",
                    "data-toggle": "toggle",
                    "data-on": "Yes",
                    "data-off": "No!",
                    "data-onstyle": "success",
                    "data-offstyle": "danger",
                }
            ),
            "info_birthday": DateInput(attrs={"type": "date", "format": "%d-%m-%Y"}),
            "social_instagram": URLInput(),
            "social_facebook": URLInput(),
            "social_twitter": URLInput(),
            "social_spotify": URLInput(),
        }

    def clean(self):
        # Call the custom validator function
        validate_age(self)
        validate_username(self)
        validate_email(self)


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
        labels = {
            "info_name": "Sock's name",
            "info_about": "Sock's story to tell",
            "info_color": "Sock's color",
            "info_fabric": "What's the sock made of",
            "info_fabric_thickness": "How thick is the material",
            "info_brand": "What is the brand",
            "info_type": "Which type is it",
            "info_size": "Which size is it",
            "info_age": "How old in years is it",
            "info_separation_date": "When did it split up",
            "info_condition": "What is its condition",
            "info_holes": "How many holes has it got",
            "info_kilometers": "How many kilometers has it walked so far",
            "info_inoutdoor": "Which environment was it used in",
            "info_washed": "How often was it washed per week",
            "info_special": "What is the one special thing",
        }

        widgets = {
            "info_separation_date": DateInput(
                attrs={"type": "date", "format": "%d-%m-%Y"}
            ),
            "info_age": RangeInput(
                attrs={
                    "type": "range",
                    "min": "0",
                    "max": "25",
                    "step": "1",
                    "value": 0,
                }
            ),
            "info_holes": RangeInput(
                attrs={
                    "type": "range",
                    "min": "0",
                    "max": "10",
                    "step": "1",
                    "value": 0,
                }
            ),
            "info_kilometers": RangeInput(
                attrs={
                    "type": "range",
                    "min": "0",
                    "max": "1000",
                    "step": "1",
                    "value": 0,
                }
            ),
            "info_washed": RangeInput(
                attrs={"type": "range", "min": "0", "max": "7", "step": "1", "value": 0}
            ),
        }


class SockProfilePictureForm(ModelForm):
    class Meta:
        model = SockProfilePicture
        fields = "__all__"
        exclude = ["sock"]
