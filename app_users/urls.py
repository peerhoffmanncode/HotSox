from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.user_signup, name="signup"),
    path("edit/<int:pk>", views.user_edit, name="edit"),
]
