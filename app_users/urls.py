from django.urls import path
from . import views

app_name = "app_users"
urlpatterns = [
    path("signup/", views.user_signup, name="signup"),
    path("edit/<int:pk>", views.user_edit, name="edit"),
    path("check_user_validation/", views.user_validate, name="validate"),

]
