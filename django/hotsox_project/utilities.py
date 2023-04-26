from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from app_users.models import User
import datetime


def create_db_entry_social_app(
    site_name, site_domain, provider, name, client_id, secret
):
    created = False
    try:
        site = Site.objects.get(domain=site_domain)
        if site.domain != site_domain:
            site.domain = site_domain
            site.save()
    except Site.DoesNotExist:
        site = Site.objects.create(domain=site_domain, name=site_name)

    try:
        # Check if a social application with the given provider name
        # already exists
        social_app = SocialApp.objects.get(provider=provider)
        if social_app.client_id != client_id or social_app.secret != secret:
            social_app.client_id = client_id
            social_app.secret = secret
            social_app.save()
            created = True
    except SocialApp.DoesNotExist:
        # If the social application does not exist, create it
        social_app = SocialApp.objects.create(
            provider=provider, name=name, client_id=client_id, secret=secret
        )
        social_app.sites.add(site)
        social_app.save()

    # Checks if there are any users in the database. If not, uses env file
    # details to create a superuser (so admin panel can be accessed)
    if len(User.objects.all()) == 0 and os.environ.get("ADMIN_USERNAME"):
        User.objects.create_superuser(
            username=os.environ.get("ADMIN_USERNAME", None),
            password=os.environ.get("ADMIN_PWD", None),
            email="admin@admin.com",
            info_birthday=datetime.date(2000, 1, 1),
            info_gender="1",
            location_city="Berlin",
            notification=True,
        )

    # return current SITE_ID
    return created, Site.objects.get(domain=site_domain).id
