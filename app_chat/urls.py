from django.urls import path
from . import views


app_name = "app_chat"
urlpatterns = [path("<str:matched_user_name>", views.chat_with_match, name="chat")]
