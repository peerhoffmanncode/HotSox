from django.urls import path
from . import views

app_name = "app_home"
urlpatterns = [
    path("", views.home, name="home"),
    path("prove-of-concept/", views.prove_of_concept, name="to_be_deleted"),
]
