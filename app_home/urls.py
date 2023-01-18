from django.urls import path
from . import views

app_name = "app_home"
urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("swipe/", views.SwipeView.as_view(), name="swipe"),
]
