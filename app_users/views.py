from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .models import User, UserProfilePicture
from .forms import UserSignUpForm, UserProfileForm, UserProfilePictureForm


def user_signup(request):
    """View to sign up a new user.
    We will gather information from from.UserSignUpForm
    Next store this new user to the db via ORM and then
    login() then newly created user
    """
    if request.method == "POST":
        form_user_profile = UserSignUpForm(request.POST)

        if form_user_profile.is_valid():
            # create a user object from the form
            user = form_user_profile.save(commit=False)

            # fix the data
            user.first_name = form_user_profile.cleaned_data["first_name"].title()
            user.last_name = form_user_profile.cleaned_data["last_name"].title()

            # check if user is ate least 18 years old
            if user.is_18_years():
                # store the user to the database
                user.save()
                # log user in via django login
                login(request, user)
                # redirect to user profile picture page
                return redirect(reverse("app_users:user-profile-picture"))
            else:
                print(
                    "sorry, grow up... User:",
                    user.username,
                    "you need to be at least 18 years old!",
                )
                return render(
                    request,
                    "users/signup.html",
                    {
                        "form_user_profile": form_user_profile,
                    },
                )
    else:
        form_user_profile = UserSignUpForm()

    # show user signup page
    return render(
        request,
        "users/signup.html",
        {
            "form_user_profile": form_user_profile,
        },
    )


@login_required(login_url="/user/login")
def user_profile_details(request):
    """View to show the details new user."""

    user_to_update = get_object_or_404(User, pk=request.user.pk)
    return render(
        request,
        "users/profile_details.html",
        {"user": user_to_update},
    )


@login_required(login_url="/user/login")
def user_profile_update(request):
    """View to edit a new user.
    We will gather information from from.UserSignUpForm
    Next store this new user to the db via ORM and then
    Authenticate() then user
    """

    user_to_update = get_object_or_404(User, pk=request.user.pk)

    if request.method == "POST":
        form_user_profile = UserProfileForm(request.POST, instance=user_to_update)

        if form_user_profile.is_valid():
            # check if user is >18 years old

            if user_to_update.is_18_years():
                # store the user to the database
                user_to_update = form_user_profile.save()
                # log user in via django login
                login(request, user_to_update)
                # redirect to user profile details page
                return redirect(reverse("app_users:user-profile-details"))
            else:
                print(
                    "sorry, grow up... User:",
                    user_to_update.username,
                    "you need to be at least 18 years old!",
                )
                return redirect(reverse("app_users:user-profile-update"))

    else:
        form_user_profile = UserProfileForm(instance=user_to_update)

    # show user profile update page
    return render(
        request,
        "users/profile_update.html",
        {
            "form_user_profile": form_user_profile,
        },
    )


@login_required(login_url="/user/login")
def user_profile_picture(request):
    """View to edit/add a new profile picture to a user."""
    # get current user
    user_to_update = get_object_or_404(User, pk=request.user.pk)
    # get all profile pictures from current user
    profile_picture_query_set = user_to_update.profile_picture.all()

    # check if profile_picture_query_set is not True
    if not profile_picture_query_set:
        profile_picture_query_set = [""]

    if request.method == "POST":
        form_user_profile_picture = UserProfilePictureForm(
            request.POST,
            request.FILES,
            initial={"user": user_to_update},
        )

        if form_user_profile_picture.is_valid():
            # create a profile_picture object
            new_profile_picture = form_user_profile_picture.save(commit=False)
            # set one to many field [user] to current user
            new_profile_picture.user = user_to_update
            # store the picture to the database
            new_profile_picture.save()
            # redirect to user profile details page
            return redirect(reverse("app_users:user-profile-details"))

    else:
        form_user_profile_picture = UserProfilePictureForm(
            initial={
                "user": user_to_update,
                "profile_picture_query_set": profile_picture_query_set,
            },
        )

    # show user profile picture page
    return render(
        request,
        "users/profile_picture.html",
        {
            "profile_picture_query_set": profile_picture_query_set,
            "form_user_profile_picture": form_user_profile_picture,
        },
    )


@login_required(login_url="/user/login")
def user_validate(request):
    """View to validate a new user.
    if user information are missing, redirect to profile page.
    """
    current_user = get_object_or_404(User, pk=request.user.pk)

    if not current_user.is_18_years():
        return redirect(reverse("app_users:user-profile-update"))
    else:
        return redirect(reverse("app_home:index"))
