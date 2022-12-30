from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .models import User
from .forms import UserSignUpForm, UserEditForm


def user_signup(request):
    """View to sign up a new user.
    We will gather information from from.UserSignUpForm
    Next store this new user to the db via ORM and then
    login() then newly created user
    """
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            # create a user object from the form
            user = form.save(commit=False)

            # fix the data
            user.first_name = form.cleaned_data["first_name"].title()
            user.last_name = form.cleaned_data["last_name"].title()

            # check if user is ate least 18 years old
            if user.is_18_years():
                # store the user to the database
                user.save()
                # log user in via django login
                login(request, user)
                # redirect to home page
                return redirect("/")
            else:
                print(
                    "sorry, grow up... User:",
                    user.username,
                    "you need to be at least 18 years old!",
                )
                return render(request, "registration/signup.html", {"form": form})
    else:
        form = UserSignUpForm()
    # show user signup page
    return render(request, "registration/signup.html", {"form": form})


@login_required(login_url="/user/login")
def user_edit(request, pk):
    """View to edit a new user.
    We will gather information from from.UserSignUpForm
    Next store this new user to the db via ORM and then
    Authenticate() then user
    """

    # check if current user is allowed to edit this user
    user_to_update = get_object_or_404(User, pk=pk)

    if request.user.username != user_to_update.username:
        # return to home
        return redirect("/")

    if request.method == "POST":
        form = UserEditForm(request.POST, initial=user_to_update.to_json())
        if form.is_valid():

            # store the data in user object
            user_to_update.first_name = form.cleaned_data["first_name"].title()
            user_to_update.last_name = form.cleaned_data["last_name"].title()
            user_to_update.email = form.cleaned_data["email"]
            user_to_update.birthday = form.cleaned_data["birthday"]
            user_to_update.user_sex = form.cleaned_data["user_sex"]
            user_to_update.interested_sex = form.cleaned_data["interested_sex"]

            # check if user is ate least 18 years old
            if user_to_update.is_18_years():
                # store the user to the database
                user_to_update.save()
                # log user in via django login
                login(request, user_to_update)
                # redirect to home page
                return redirect("/")
            else:
                print(
                    "sorry, grow up... User:",
                    user_to_update.username,
                    "you need to be at least 18 years old!",
                )
                return redirect(
                    reverse("app_users:edit", kwargs={"pk": user_to_update.pk})
                )
    else:
        form = UserEditForm(initial=user_to_update.to_json())
    # show user signup page
    return render(request, "registration/edit.html", {"form": form})


@login_required(login_url="/")
def user_validate(request):
    """View to validate a new user.
    if user information are missing, redirect to profile page.
    """
    # breakpoint()

    # check if current user is allowed to edit this user
    current_user = get_object_or_404(User, pk=request.user.pk)

    if (
        not current_user.is_18_years()
        or not current_user.user_sex
        or not current_user.interested_sex
    ):
        return redirect(reverse("app_users:edit", kwargs={"pk": current_user.pk}))
    else:
        return redirect(reverse("app_home:home"))
