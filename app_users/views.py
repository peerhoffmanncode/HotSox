from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login

from django.views.generic import TemplateView, DetailView

from .validator import HotSoxLogInAndValidationCheckMixin
from .models import User, UserProfilePicture, Sock, SockProfilePicture
from .forms import (
    UserSignUpForm,
    UserProfileForm,
    UserProfilePictureForm,
    SockProfileForm,
    SockProfilePictureForm,
)


class UserSignUp(TemplateView):
    """View to sign up a new user.
    We will gather information from from.UserSignUpForm
    Next store this new user to the db via ORM and then
    login() then newly created user
    """

    model = User
    template_name = "users/signup.html"

    def post(self, request, *args, **kwargs):
        form_user_profile = UserSignUpForm(request.POST)

        if form_user_profile.is_valid():
            # create a user object from the form
            user = form_user_profile.save(commit=False)
            # fix the data
            user.first_name = form_user_profile.cleaned_data["first_name"].title()
            user.last_name = form_user_profile.cleaned_data["last_name"].title()
            # store the user to the database
            user.save()
            # log user in via django login
            login(request, user)
            # redirect to user profile picture page
            return redirect(reverse("app_users:user-profile-picture"))
        # in case of invalid go here
        return redirect(reverse("app_users:user-signup"))

    def get(self, request, *args, **kwargs):
        form_user_profile = UserSignUpForm()

        # show user signup page
        return render(
            request,
            "users/signup.html",
            {
                "form_user_profile": form_user_profile,
            },
        )


class UserProfileDetails(HotSoxLogInAndValidationCheckMixin, TemplateView):
    """View to show a user's details."""

    model = User
    template_name = "users/profile_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["left_arrow_go_to_url"] = ""  # reverse("app_home:index")
        context["right_arrow_go_to_url"] = reverse("app_users:user-profile-update")
        return context


class UserProfileUpdate(TemplateView):
    """View to edit details of a user.
    We will gather information from from.UserSignUpForm
    we  store this user to the db via ORM and try to
    login() then user!
    This View is not protected by the LoginMixIn!
    It needs to be available for users who are not validated!
    """

    model = User
    template_name = "users/profile_update.html"

    def post(self, request, *args, **kwargs):
        user_to_update = get_object_or_404(User, pk=request.user.pk)
        form_user_profile = UserProfileForm(request.POST, instance=user_to_update)

        if form_user_profile.is_valid():
            # store the user to the database
            user_to_update = form_user_profile.save()
            # log user in via django login
            login(request, user_to_update)
            # redirect to user profile details page
            return redirect(reverse("app_users:user-profile-details"))
        # in case of invalid go here
        return redirect(reverse("app_users:user-profile-update"))

    def get(self, request, *args, **kwargs):
        user_to_update = get_object_or_404(User, pk=request.user.pk)
        form_user_profile = UserProfileForm(instance=user_to_update)

        # show user profile update page
        return render(
            request,
            "users/profile_update.html",
            {
                "form_user_profile": form_user_profile,
                "left_arrow_go_to_url": reverse("app_users:user-profile-details"),
                "right_arrow_go_to_url": reverse("app_users:sock-overview"),
            },
        )


class UserProfilePictureUpdate(HotSoxLogInAndValidationCheckMixin, TemplateView):
    """View to edit/add a new profile picture to a user."""

    model = User
    template_name = "users/profile_picture.html"

    def post(self, request, *args, **kwargs):
        # get current user
        user_to_update = get_object_or_404(User, pk=request.user.pk)
        # get all profile pictures from current user
        profile_picture_query_set = user_to_update.get_all_pictures()

        # check if profile_picture_query_set is not True
        if not profile_picture_query_set:
            profile_picture_query_set = [""]

        if request.POST.get("method") == "delete":
            # delete the selected picture!
            picture_pk = request.POST.get("picture_pk", None)
            if picture_pk:
                UserProfilePicture_obj = UserProfilePicture.objects.get(pk=picture_pk)
                UserProfilePicture_obj.delete()
                return redirect(reverse("app_users:user-profile-picture"))

        elif request.POST.get("method") == "add":
            # add the selected picture!
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
                return redirect(reverse("app_users:user-profile-picture"))
            # in case of invalid go here
            return redirect(reverse("app_users:user-profile-picture"))

    def get(self, request, *args, **kwargs):
        # get current user
        user_to_update = get_object_or_404(User, pk=request.user.pk)
        # get all profile pictures from current user
        profile_picture_query_set = user_to_update.get_all_pictures()
        # create form
        form_user_profile_picture = UserProfilePictureForm(
            initial={
                "user": user_to_update,
            },
        )

        # show user profile picture page
        return render(
            request,
            "users/profile_picture.html",
            {
                "profile_picture_query_set": profile_picture_query_set,
                "form_user_profile_picture": form_user_profile_picture,
                "left_arrow_go_to_url": "",
                "right_arrow_go_to_url": reverse("app_users:user-profile-details"),
            },
        )


class SockProfileOverview(HotSoxLogInAndValidationCheckMixin, TemplateView):
    """View to show all socks's of a User."""

    model = User
    template_name = "users/sock_overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["left_arrow_go_to_url"] = reverse("app_users:user-profile-update")
        context["right_arrow_go_to_url"] = ""
        return context

    def post(self, request, *args, **kwargs):
        # get current user

        if request.POST.get("method") == "delete":
            # delete the selected picture!
            sock_pk = request.POST.get("sock_pk", None)

            if sock_pk:
                breakpoint()
                sock_obj = get_object_or_404(Sock, pk=request.POST.get("sock_pk"))
                sock_obj.delete()
                return redirect(reverse("app_users:sock-overview"))

        elif request.POST.get("method") == "add":
            # add the selected picture!
            return redirect(reverse("app_users:sock-create"))


class SockProfileDetails(HotSoxLogInAndValidationCheckMixin, DetailView):
    """View to show a socks's details."""

    model = Sock
    template_name = "users/sock_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["left_arrow_go_to_url"] = reverse("app_users:sock-overview")
        context["right_arrow_go_to_url"] = reverse(
            "app_users:sock-update", kwargs={"pk": kwargs["object"].pk}
        )
        return context


class SockProfileCreate(HotSoxLogInAndValidationCheckMixin, TemplateView):
    """Add a new sock.
    We will gather information from from.SockForm
    Next store this sock to the db via ORM"""

    model = Sock
    template_name = "users/sock_update.html"
    # 1. redirect to sock_update form. User fills in and submits

    def get(self, request):
        form_sock_profile = SockProfileForm(initial={"user": request.user})

        # show sock profile update page
        return render(
            request,
            "users/sock_update.html",
            {
                "form_sock_profile": form_sock_profile,
                "sock": "",
                "left_arrow_go_to_url": "",
                "right_arrow_go_to_url": "",
            },
        )

    def post(self, request):
        form_sock_profile = SockProfileForm(
            request.POST, initial={"user": request.user}
        )

        if form_sock_profile.is_valid():
            # store the sock to the database
            sock_to_add = form_sock_profile.save(commit=False)
            sock_to_add.user = request.user
            sock_to_add.save()
            # redirect to sock profile details page
            return redirect(
                reverse("app_users:sock-picture", kwargs={"pk": sock_to_add.pk})
            )
        # in case of invalid go here
        return redirect(reverse("app_users:sock-create"))


class SockProfileUpdate(HotSoxLogInAndValidationCheckMixin, TemplateView):
    """View to edit a sock.
    We will gather information from from.SockForm
    Next store this sock to the db via ORM
    """

    model = Sock
    template_name = "users/sock_update.html"

    def post(self, request, pk):
        sock_to_update = get_object_or_404(Sock, pk=pk)
        form_sock_profile = SockProfileForm(request.POST, instance=sock_to_update)

        if form_sock_profile.is_valid():
            # store the sock to the database
            sock_to_update = form_sock_profile.save()
            # redirect to sock profile details page
            return redirect(
                reverse("app_users:sock-details", kwargs={"pk": sock_to_update.pk})
            )
        # in case of invalid go here
        return redirect(
            reverse("app_users:sock-update", kwargs={"pk": sock_to_update.pk})
        )

    def get(self, request, pk):

        sock_to_update = get_object_or_404(Sock, pk=pk)
        form_sock_profile = SockProfileForm(instance=sock_to_update)

        # show sock profile update page
        return render(
            request,
            "users/sock_update.html",
            {
                "form_sock_profile": form_sock_profile,
                "sock": sock_to_update,
                "left_arrow_go_to_url": reverse(
                    "app_users:sock-details", kwargs={"pk": sock_to_update.pk}
                ),
                "right_arrow_go_to_url": "",
            },
        )


class SockProfilePictureUpdate(HotSoxLogInAndValidationCheckMixin, TemplateView):
    """View to edit/add a new profile picture to a user."""

    model = Sock
    template_name = "users/sock_picture.html"

    def post(self, request, pk):
        # get current user
        sock_to_update = get_object_or_404(Sock, pk=pk)
        # get all profile pictures from current user
        profile_picture_query_set = sock_to_update.get_all_pictures()

        # check if profile_picture_query_set is not True
        if not profile_picture_query_set:
            profile_picture_query_set = [""]

        if request.POST.get("method") == "delete":
            # delete the selected picture!
            picture_pk = request.POST.get("picture_pk", None)
            if picture_pk:
                SockProfilePicture_obj = SockProfilePicture.objects.get(pk=picture_pk)
                SockProfilePicture_obj.delete()
                return redirect(
                    reverse("app_users:sock-picture", kwargs={"pk": sock_to_update.pk})
                )

        elif request.POST.get("method") == "add":
            # add the selected picture!
            form_sock_profile_picture = SockProfilePictureForm(
                request.POST,
                request.FILES,
                initial={"sock": sock_to_update},
            )
            if form_sock_profile_picture.is_valid():
                # create a profile_picture object
                new_profile_picture = form_sock_profile_picture.save(commit=False)
                # set one to many field [user] to current user
                new_profile_picture.sock = sock_to_update
                # store the picture to the database
                new_profile_picture.save()
                # redirect to user profile details page
                return redirect(
                    reverse("app_users:sock-picture", kwargs={"pk": sock_to_update.pk})
                )
            # in case of invalid go here
            return redirect(
                reverse("app_users:sock-picture", kwargs={"pk": sock_to_update.pk})
            )

    def get(self, request, pk):
        # get current user
        sock_to_update = get_object_or_404(Sock, pk=pk)
        # get all profile pictures from current user
        profile_picture_query_set = sock_to_update.get_all_pictures()
        # create form
        form_sock_profile_picture = SockProfilePictureForm(
            initial={
                "sock": sock_to_update,
            },
        )

        # show user profile picture page
        return render(
            request,
            "users/sock_picture.html",
            {
                "profile_picture_query_set": profile_picture_query_set,
                "form_sock_profile_picture": form_sock_profile_picture,
                "sock": sock_to_update,
            },
        )
