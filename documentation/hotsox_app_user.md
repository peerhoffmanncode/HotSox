# HOTSOX "app_users"

The "app_user" of the HotSox Project is composed by different features that handles the User Profiles and their related Socks profile/s.

## MAIN FEATURE: Login and User CRUD using “Django AllAuth”

### Purpose

The purpose/ aim of the feature is to give the user the option to register and/or sign in/out (or edit) preferences with the app alonside to create edit and manage socks profile information.

### Description

A user can signup to the app by entering his personal information and attributes from username, password to age and city where the user lives in.
During this signup process we lookup the geolocation (see geo_app documentation for details) from the given city name. Everything will be stored to our database as the main user model.
Using AllAuth we do not have to create the whole authentication process but relay on what is done by this package.
A user can upload one or many profile picture/s which will be stored to the cloudinary CDN service. We use their python SDK packet to make it most convenient for our development experience [https://cloudinary.com/documentation/python_quickstart]. This SDK includes a Django ready model field as a specific “picture upload field”.
Users can edit their profiles as well as add or remove pics from their profile pictures.

A user can see a profile overview that shows all his/her personal data as well as a visual representation of his geo location on a map created by folium. As a part of this overview a user is also able to delete his/her account. An account deletion will also delete any related data (socks, pictures, messages, chats) from the database.

A user can create an account at hotsox using the social media login via Oatuth2.0 via google. He/she needs to have a valid account at google. Validation and password hashing is done by google automatically.

### Technical implementation

The whole app is designed around the logged-in user. Every aspect of the app, every functionality, every backend or frontend part is validating that a given user has the permission to do a certain action. A logged in user can only see him-/herself, its own socks, and all actions that has him/her as the center of interest. A user can only interact with another user once they have a valid match. This means you can only see, chat, interact with a users you matched.
This is done using custom validation mixing classes that inherit their main functionality from Djangos “LoginRequiredMixin” class. Every view or endpoint is protected, except the signup and login.

### UI/UX:

Our frontend uses custom forms for signup / login / and log out. The forms are designed using crispy forms as well as custom form widgets. The widgets are a custom switch to enable/ disable notifications, and sliding range selectors for any numeric input field.

### Licenses & Dependencies

Django AllAuth https://django-allauth.readthedocs.io/en/latest/
Django crispy forms https://django-crispy-forms.readthedocs.io/en/latest/
Cloudinary SDK https://cloudinary.com/documentation/python_quickstart/

## MAIN FEATURE: Database/Models

### Description of feature:

The HotSox Database is a relational DB that stores information about Users, Socks, Matches and Messages.

### Technical implementation:

This dating app is not an ordinary platform, and you can clearly see that from our database. We aimed to depart from the idea of providing everything to the user at once. Our unique "sock" plays a significant role in the app, and in order to connect with another user, one must first rummage through socks - sometimes clean, sometimes not very clean, and sometimes even smelly.

### ERD of the relevant tables of our Database:

![ERD Deagramm HotSox Database](pics/app_users/erd_diagramm_hotsox_database.png)

According to our diagram, both users must create a profile for their socks and like each other's socks in order to chat. In programming terms, this means that users need to create a “Sock” object and a “User” object, followed by a “SockLike” object that links the two. Once both users have liked each other's socks, they can create a “UserMatch” object to indicate that they are a match. Then, they can start exchanging messages using the “MessageChat” object. The “SockProfilePicture” object can be used to upload and display profile pictures for socks, while the “UserProfilePicture” object can be used for users. All of these objects are stored in the HotSox Database, a relational database implemented using the Django web framework and supported by a PostgreSQL database.

For example: code block user_app/models.py/lines33-68:

```python
	class User(AbstractUser):
        email = models.EmailField(_("email address"), blank=True, unique=True)
        info_about = models.TextField(blank=True)
        info_birthday = models.DateField(default=timezone.now, blank=False)
        info_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=False)
        ....
```

This is a Django model class called “User” which inherits from Django's built-in “AbstractUser” model.
In addition to the fields inherited from “AbstractUser” we included customs fields to give the user more information.
The User model is used as ForeignKey in other models.

e.g.: the “UserMatch” Model codeblock: user_app/models.py/lines207-235

```python
class UserMatch(models.Model):
    user = models.ForeignKey(
        User,
        related_name="user_match",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    other = models.ForeignKey(
        User,
        related_name="matched",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    ....

```

The "user" and "other" fields are foreign keys to the" User" model, representing the users who are matched. The "related_name" parameter is used to set the reverse relation names on the" User" model. The "unmatched" field is a boolean that is set to "True" when the match is no longer valid. The "chatroom_uuid" field is a UUID (Universally Unique Identifier) that is used to identify the chatroom where the matched users can communicate.

#### Dependency:

Cloudinary (https://cloudinary.com/documentation)

### SUB-FEATURE: User and Sock Models getter methods

#### Description of feature:

The getter methods sets of functions defined in the User and Sock classes that are used to retrieve specific information from a user or sock instance. These methods include get_all_pictures, get_picture_urls, get_matches, get_unmatched, get_socks, get_mail_messages, and get_chat_messages for the User model. The Sock besides get_all_pictures and get_picture_urls has its own get_likes and get_dislikes methods.
Purpose:
The purpose of these methods is to provide an easy way to retrieve specific information about a user or sock instance, without having to manually access the database.

#### Technical Implementation:

These methods are implemented using Django's QuerySet API, which provides a simple way to query the database for specific objects. Each method retrieves the relevant objects using one or more queries and returns them as a queryset or list, depending on the use case.

#### Django Authentification Model

The User Model inherit from the AbstractUser class, which is part of Django's built-in authentication system.

#### User Model Method Details:

**get_all_pictures**: Returns a queryset containing all profile pictures associated with the user instance.
**get_picture_urls**: Returns a list of URLs for all profile pictures associated with the user instance.
**get_matches**: Returns a queryset containing all matches associated with the user instance.
**get_unmatched**: Returns a queryset containing all unmatched matches associated with the user instance.
**get_socks**: Returns a queryset containing all socks associated with the user instance.
**get_mail_messages**: Returns a queryset containing all mail messages associated with the user instance.
**get_chat_messages**: Returns a queryset containing all chat messages associated with the user instance.

#### Sock Model Method Details:

**get_all_pictures**: Returns a queryset containing all profile pictures associated with the sock instance.
**get_picture_urls**: Returns a list of URLs for all profile pictures associated with the sock instance.
**get_likes**: Returns a queryset of Sock instances liked by the current Sock instance.
**get_disllikes**: Returns a queryset of Sock instances that the current Sock instance has disliked.

## MAIN FEATURE: Forms/Templates and Validation

## MAIN FEATURE: Match Overview

### NOTE: Peer will take care
