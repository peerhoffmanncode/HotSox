from django.urls import path
from . import views

urlpatterns = [path("<str:matched_user_name>", views.chat_with_match)]
