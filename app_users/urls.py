from django.urls import path
from . import views

app_name = "app_users"
urlpatterns = [
    path("signup/", views.UserSignUp.as_view(), name="user-signup"),
    path("check_user_validation/", views.user_validate, name="user-validate"),
    path(
        "profile/details",
        views.UserProfileDetails.as_view(),
        name="user-profile-details",
    ),
    path(
        "profile/update", views.UserProfileUpdate.as_view(), name="user-profile-update"
    ),
    path(
        "profile/picture",
        views.UserProfilePictureUpdate.as_view(),
        name="user-profile-picture",
    ),
    # path("matched/", views.user_matched, name="user-matched"),
    # path("sock/add/", views., name="sock-add"),
    # path("sock/profile/", views., name="sock-profile"),
    # path("sock/matched/", views., name="sock-matched"),
]
