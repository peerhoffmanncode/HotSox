# Generated by Django 4.1.4 on 2023-01-12 19:47

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app_users", "0008_alter_userprofilepicture_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofilepicture",
            name="profile_picture",
            field=cloudinary.models.CloudinaryField(
                max_length=255, verbose_name="profile picture"
            ),
        ),
    ]
