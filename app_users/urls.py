from django.urls import path
from . import views

app_name = "app_users"
urlpatterns = [
    path("signup/", views.user_signup, name="user-signup"),
    path("check_user_validation/", views.user_validate, name="user-validate"),
    path("profile/details", views.user_profile_details, name="user-profile-details"),
    path("profile/update", views.user_profile_update, name="user-profile-update"),
    path("profile/picture", views.user_profile_picture, name="user-profile-picture"),
    # path("matched/", views.user_matched, name="user-matched"),
    # path("sock/add/", views., name="sock-add"),
    # path("sock/profile/", views., name="sock-profile"),
    # path("sock/matched/", views., name="sock-matched"),
]
