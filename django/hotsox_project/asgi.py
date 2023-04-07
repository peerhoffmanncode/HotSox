"""
ASGI config for hotsox_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

# load DJANGO_SETTINGS_MODULE
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotsox_project.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# initialize main django setup
from django import setup

setup()

# load everything for ASGI runtime
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import app_chat.routing


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(app_chat.routing.websocket_urlpatterns)
        ),
    }
)

# Hook in here to create defaults for AllAuth in the database
# make sure google is stored in the socialaccount apps in the database
from asgiref.sync import sync_to_async
from django.conf import settings
from .utilities import create_db_entry_social_app

created, settings.SITE_ID = create_db_entry_social_app(
    site_name="127.0.0.1:8000",
    site_domain="127.0.0.1:8000",
    provider="google",
    name="Google",
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    secret=os.environ.get("GOOGLE_SECRET"),
)
if created:
    print("included google to AllAuth, set SITE_ID to:", settings.SITE_ID)
