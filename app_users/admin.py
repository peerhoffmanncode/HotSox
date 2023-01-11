from django.contrib import admin
from django.db.models import fields
from .models import (
    User,
    UserProfilePicture,
    UserMatch,
    Sock,
    SockProfilePicture,
    SockLike,
    MessageMail,
    MessageChat,
)


# All User models
class UserProfilePictureInLine(admin.TabularInline):
    model = UserProfilePicture
    extra = 0


class UserMatchInLine(admin.TabularInline):
    model = UserMatch
    fk_name = "user"
    extra = 0


class UserAdmin(admin.ModelAdmin):
    fields = ["username", "first_name", "last_name", "email"]
    inlines = [UserProfilePictureInLine, UserMatchInLine]


# All Sock models
class SockProfilePictureInLine(admin.TabularInline):
    model = SockProfilePicture
    extra = 0


class SockLikeInLine(admin.TabularInline):
    model = SockLike
    fk_name = "sock"
    extra = 0


class SockAdmin(admin.ModelAdmin):
    fields = [
        "user",
        "info_name",
        "info_about",
        "info_age",
        "info_brand",
        "info_color",
        "info_condition",
        "info_fabric",
        "info_fabric_thickness",
        "info_holes",
        "info_inoutdoor",
        "info_kilometers",
        "info_separation_date",
        "info_size",
        "info_special",
        "info_type",
        "info_washed",
    ]
    exclude = ["info_joining_date"]
    fk_name = "user"
    inlines = [
        SockProfilePictureInLine,
        SockLikeInLine,
    ]


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Sock, SockAdmin)
admin.site.register(MessageMail)
admin.site.register(MessageChat)
