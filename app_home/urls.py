from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("prove-of-concept/", views.prove_of_concept, name="logged_in"),
]
