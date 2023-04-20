from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password

# setup test user
TEST_USER1 = {
    "username": "admin",
    "first_name": "admin",
    "last_name": "admin",
    "email": "admin@admin.com",
    "info_about": "admin",
    "info_birthday": "0001-01-01",
    "info_gender": 1,
    "location_city": "AdminCity",
    "location_latitude": 0,
    "location_longitude": 0,
    "notification": True,
    "social_instagram": "",
    "social_facebook": "",
    "social_twitter": "",
    "social_spotify": "",
    "password": "admin",
    "is_active": True,
    "is_superuser": True,
}

TEST_USER2 = {
    "username": "testuser2",
    "first_name": "testuser2",
    "last_name": "testuser2",
    "email": "testuser2@testuser2.com",
    "info_about": "testuser2",
    "info_birthday": "1001-01-01",
    "info_gender": 2,
    "location_city": "testuser2City",
    "location_latitude": 0,
    "location_longitude": 0,
    "notification": False,
    "social_instagram": "",
    "social_facebook": "",
    "social_twitter": "",
    "social_spotify": "",
    "password": "testuser2",
    "is_active": True,
    "is_superuser": False,
}


def token(client, username: str, password: str) -> dict:
    # request JWT token
    response = client.post(
        reverse("app_restapi:token_obtain_pair"),
        data={"username": username, "password": password},
    )
    # store JWT token
    token = response.json().get("access", None)

    if token:
        # set JWT token in header
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    else:
        # unauthorized user!
        client.credentials(HTTP_AUTHORIZATION="")

    # return f"Bearer {token}"
