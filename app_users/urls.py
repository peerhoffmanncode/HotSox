from django.urls import path
from . import views

app_name = "app_users"
urlpatterns = [
    path("signup/", views.UserSignUp.as_view(), name="user-signup"),
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
    path("sock/overview/", views.SockProfileOverview.as_view(), name="sock-overview"),
    path(
        "sock/<int:pk>/details/",
        views.SockProfileDetails.as_view(),
        name="sock-details",
    ),
    path(
        "sock/create/",
        views.SockProfileCreate.as_view(),
        name="sock-create",
    ),
    path(
        "sock/<int:pk>/update/",
        views.SockProfileUpdate.as_view(),
        name="sock-update",
    ),
    path(
        "sock/<int:pk>/picture/",
        views.SockProfilePictureUpdate.as_view(),
        name="sock-picture",
    ),
    # path("sock/matched/", views., name="sock-matched"),
]
