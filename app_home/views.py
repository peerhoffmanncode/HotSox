from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from app_users.models import HotSoxUserModel


def home(request):
    if request.user.username:
        user = HotSoxUserModel.objects.get(username=request.user.username)
        user.username = user.username.title()
        context = {"user": user.to_json()}
    else:
        context = {"user": None}

    return render(request, "app_home/index.html", context)


@login_required(login_url="/user/login")
def prove_of_concept(request):
    return HttpResponse(
        f"<h1>Seems like you are logged in! Yeay! </h1><p>Nice job {str(request.user.username).title()}!</p>"
    )
