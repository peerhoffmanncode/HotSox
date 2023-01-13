from django.urls import path
from . import views

app_name = "app_home"
urlpatterns = [
    path("", views.home, name="index"),
    path("about/", views.about, name="about"),
    path("swipe/", views.swipe, name="swipe"),
    path("prove-of-concept/", views.prove_of_concept, name="to_be_deleted"),
]
