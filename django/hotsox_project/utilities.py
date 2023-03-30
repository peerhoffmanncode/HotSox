from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


def create_db_entry_social_app(
    site_name, site_domain, provider, name, client_id, secret
):
    try:
        site = Site.objects.get(domain=site_domain)
        if site.domain != site_domain:
            site.domain = site_domain
            site.save()
    except Site.DoesNotExist:
        site = Site.objects.create(domain=site_domain, name=site_name)

    try:
        # Check if a social application with the given provider name already exists
        social_app = SocialApp.objects.get(provider=provider)
        if social_app.client_id != client_id or social_app.secret != secret:
            social_app.client_id = client_id
            social_app.secret = secret
            social_app.save()
    except SocialApp.DoesNotExist:
        # If the social application does not exist, create it
        social_app = SocialApp.objects.create(
            provider=provider, name=name, client_id=client_id, secret=secret
        )
        social_app.sites.add(site)
        social_app.save()

    # return current SITE_ID
    return Site.objects.get(domain=site_domain).id
