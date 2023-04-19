from unittest import mock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import warnings
from fastapi_pagination.utils import FastAPIPaginationWarning

warnings.simplefilter("ignore", FastAPIPaginationWarning)

from .inital_test_setup import (
    client,
    PREFIX,
    TEST_USER1,
    TEST_USER2,
    test_db_setup,
    mock_upload_file,
    token,
)


# setup a test database for the test
from api.authentication.hashing import Hash
from api.database.models import User, Sock, MessageMail, MessageChat
from api.database.setup import engine


def test_show_users_login_incorrect_cedentials(test_db_setup):
    response = client.get(PREFIX + "/users")
    assert response.status_code == 401


def test_show_users_login_incorrect_permission(test_db_setup):
    response = client.get(PREFIX + "/users", headers=token("testuser2", "testuser2"))
    assert response.status_code == 403


def test_show_users_login_correct_cedentials(test_db_setup):
    response = client.get(PREFIX + "/users", headers=token("admin", "admin"))
    content = response.json()["items"]
    assert response.status_code == 200
    assert len(content) == 2
    assert content[0].get("username") == "testuser2"
    assert content[1].get("username") == "admin"


def test_show_user_admin(test_db_setup):
    response = client.get(PREFIX + "/user", headers=token("admin", "admin"))
    assert response.status_code == 200
    # check for correct user
    with Session(engine) as db:
        db_user = db.query(User).filter(User.username == "admin").first()
        assert db_user
        for key in TEST_USER1.keys():
            if key != "password":
                assert key in db_user.__dict__.keys()


def test_show_user_that_do_not_exist(test_db_setup):
    response = client.get(PREFIX + "/user", headers=token("DoNotExist", "DoNotExist"))
    assert response.status_code == 401
    # test database if user really do not exist
    with Session(engine) as db:
        db_user = db.query(User).filter(User.username == "DoNotExist").first()
        assert db_user == None


def test_update_user_admin(test_db_setup):
    update_data = {
        "username": "admin",
        "first_name": "UPDATED1",
        "last_name": "UPDATED2",
        "email": "admin@admin.com",
        "info_about": "admin",
        "info_birthday": "1001-01-01",
        "info_gender": 1,
        "location_city": "AdminCity",
        "location_latitude": 0,
        "location_longitude": 0,
        "notification": True,
        "social_instagram": "UPDATE4",
        "social_facebook": "",
        "social_twitter": "",
        "social_spotify": "UPDATE3",
    }

    response = client.put(
        PREFIX + "/user", json=update_data, headers=token("admin", "admin")
    )
    assert response.status_code == 202
    assert response.json() == update_data
    # check that the user is updated in the database
    with Session(engine) as db:
        db_user = db.query(User).filter(User.username == "admin").first()
        assert db_user
        assert db_user.username == update_data["username"]
        assert db_user.first_name == update_data["first_name"]
        assert db_user.last_name == update_data["last_name"]
        assert db_user.social_instagram == update_data["social_instagram"]
        assert db_user.social_spotify == update_data["social_spotify"]


def test_update_user_that_do_not_exist(test_db_setup):
    update_data = {
        "username": "admin",
        "first_name": "UPDATED1",
        "last_name": "UPDATED2",
        "email": "admin@admin.com",
        "info_about": "admin",
        "info_birthday": "1001-01-01",
        "info_gender": 1,
        "location_city": "AdminCity",
        "location_latitude": 0,
        "location_longitude": 0,
        "notification": True,
        "social_instagram": "UPDATE4",
        "social_facebook": "",
        "social_twitter": "",
        "social_spotify": "UPDATE3",
    }

    response = client.put(
        PREFIX + "/user/DoNotExist", json=update_data, headers=token("admin", "admin")
    )
    assert response.status_code == 404
    # check that the user do not exist in the database
    with Session(engine) as db:
        db_user = db.query(User).filter(User.username == "DoNotExist").first()
        assert db_user == None


def test_create_user_wrong_data(test_db_setup):
    create_data = {
        "username": "bibo",
        "first_name": "bibo",
        "last_name": "bibo",
        "email": "bibo@bibo.com",
        "info_about": "bibo",
        "info_birthday": "2001-01-01",
        "info_gender": 4,
        "location_city": "biboCity",
        "location_latitude": 50,
        "location_longitude": 8,
        "notification": True,
        "social_instagram": "bibo social 1",
        "social_facebook": "bibo social 2",
        "social_twitter": "bibo social 3",
        "social_spotify": "bibo social 4",
    }

    response = client.post(PREFIX + "/user", json=create_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"
    assert response.json()["detail"][0]["type"] == "value_error.missing"
    assert response.json()["detail"][0]["loc"][1] == "password"
    # check if element exists in the database
    with Session(engine) as db:
        db_user = (
            db.query(User).filter(User.username == create_data["username"]).first()
        )
        assert db_user == None


def test_create_user_new(test_db_setup):
    create_data = {
        "username": "bibo",
        "first_name": "bibo",
        "last_name": "bibo",
        "email": "bibo@bibo.com",
        "info_about": "bibo",
        "info_birthday": "2001-01-01",
        "info_gender": 4,
        "location_city": "biboCity",
        "location_latitude": 50,
        "location_longitude": 8,
        "notification": True,
        "social_instagram": "bibo social 1",
        "social_facebook": "bibo social 2",
        "social_twitter": "bibo social 3",
        "social_spotify": "bibo social 4",
        "password": "bibobibo",
    }

    response = client.post(PREFIX + "/user", json=create_data)
    assert response.status_code == 201
    assert Hash.verify(
        response.json()["password"],
        create_data["password"],
    )
    create_data["password"] = response.json()["password"]
    assert response.json() == create_data
    # check if element exists in the database
    with Session(engine) as db:
        db_user = (
            db.query(User).filter(User.username == create_data["username"]).first()
        )
        assert db_user


def test_create_user_dupliceate(test_db_setup):
    create_data = {
        "username": "bibo",
        "first_name": "bibo",
        "last_name": "bibo",
        "email": "bibo@bibo.com",
        "info_about": "bibo",
        "info_birthday": "2001-01-01",
        "info_gender": 4,
        "location_city": "biboCity",
        "location_latitude": 50,
        "location_longitude": 8,
        "notification": True,
        "social_instagram": "bibo social 1",
        "social_facebook": "bibo social 2",
        "social_twitter": "bibo social 3",
        "social_spotify": "bibo social 4",
        "password": "bibobibo",
    }
    # create new user
    response = client.post(PREFIX + "/user", json=create_data)
    assert response.status_code == 201
    with Session(engine) as db:
        db_user = (
            db.query(User).filter(User.username == create_data["username"]).first()
        )
        assert db_user
    # check for duplicate username
    response = client.post(PREFIX + "/user", json=create_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists! <bibo>"}
    # check for duplicate email adress
    create_data["username"] = "new_name"
    response = client.post(PREFIX + "/user", json=create_data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "eMail address already exists! <bibo@bibo.com>"
    }


@mock.patch("api.database.models.destroy_profilepicture_on_cloud")
def test_delete_user(mock_celery, test_db_setup):
    mock_celery.return_value = {"message": f"user profile picture was deleted"}

    response = client.request(
        "DELETE",
        PREFIX + "/user",
        headers=token("admin", "admin"),
    )
    assert response.status_code == 204
    # check if element done not exists in the database
    with Session(engine) as db:
        db_user = db.query(User).filter(User.username == "admin").first()
        assert db_user == None


@mock.patch("api.database.models.destroy_profilepicture_on_cloud")
def test_delete_noneexisting_user(mock_celery, test_db_setup):
    mock_celery.return_value = {"message": f"user profile picture was deleted"}

    response = client.request(
        "DELETE",
        PREFIX + "/user",
        headers=token("DoNotExist", "DoNotExist"),
    )
    assert response.status_code == 401
