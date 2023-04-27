from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.authtoken.views import obtain_auth_token

# Swagger configuration
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.urls import path
from . import views_users, views_mail, views_chat, views_socks, views_swipe


app_name = "app_restapi"
urlpatterns = [
    # Swagger and ReDoc Documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="app_restapi:schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="app_restapi:schema"),
        name="redoc",
    ),
    # authentication django token
    path("django-token/", obtain_auth_token, name="api_token_auth"),
    # authentication (JWT)
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Users
    path("users/", views_users.ApiGetUsers.as_view(), name="api_user_list"),
    path(
        "user/", views_users.ApiGetPutCreateDeleteUser.as_view(), name="api_user_crud"
    ),
    # Users profile pictures
    path(
        "user/profilepic",
        views_users.ApiCreateProfilePic.as_view(),
        name="api_user_profilepic_create",
    ),
    path(
        "user/profilepic/<int:pk>",
        views_users.ApiDeleteProfilePic.as_view(),
        name="api_user_profilepic_delete",
    ),
    # Mail
    path("user/mail/", views_mail.ApiGetMails.as_view(), name="api_mail_listsend"),
    path(
        "user/mail/<int:pk>/",
        views_mail.ApiDeleteMail.as_view(),
        name="api_mail_delete",
    ),
    # Chat
    path("user/chats/", views_chat.ApiGetChats.as_view(), name="api_chats_list"),
    path(
        "user/chat/<str:receiver>/",
        views_chat.ApiGetSendChat.as_view(),
        name="api_chat_get_send",
    ),
    # Socks
    path("user/socks/", views_socks.ApiGetSocks.as_view(), name="api_sock_list"),
    path(
        "user/sock/<int:pk>/",
        views_socks.ApiGetPutDeleteSock.as_view(),
        name="api_sock_rud",
    ),
    path("user/sock/", views_socks.ApiCreateSock.as_view(), name="api_sock_create"),
    # Sock picture
    path(
        "user/sock/<int:sock_id>/profilepic/",
        views_socks.ApiCreateSockProfilePic.as_view(),
        name="api_sock_profilepic_create",
    ),
    path(
        "user/sock/<int:sock_id>/profilepic/<int:pic_id>",
        views_socks.ApiDeleteSockProfilePic.as_view(),
        name="api_sock_profilepic_delete",
    ),
    # Swipe
    path(
        "user/swipe/<int:sock_id>/next",
        views_swipe.ApiSwipeNextSock.as_view(),
        name="api_next_sock",
    ),
    path(
        "user/swipe/<int:sock_id>/judge/<int:other_sock_id>",
        views_swipe.ApiJudgeSock.as_view(),
        name="api_judge_sock",
    ),
    # Match
]
