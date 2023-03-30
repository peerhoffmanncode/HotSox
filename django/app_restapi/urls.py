from django.urls import path
from . import views

app_name = "app_restapi"
urlpatterns = [
    path("users/", views.ApiGetUsers.as_view(), name="api_user_list"),
    path("user/<int:pk>/", views.ApiGetUser.as_view(), name="api_user_detail"),
    path("user/mails/", views.ApiGetMails.as_view(), name="api_mail_list"),
    path("user/mail/<int:pk>/", views.ApiGetMail.as_view(), name="api_mail_detail"),
    path("user/chats/", views.ApiGetChats.as_view(), name="api_chats_list"),
    path("user/chat/<int:pk>/", views.ApiGetChat.as_view(), name="api_chat_detail"),
    path("user/socks/", views.ApiGetSocks.as_view(), name="api_sock_list"),
    path("user/sock/<int:pk>/", views.ApiGetSock.as_view(), name="api_sock_detail"),
]
