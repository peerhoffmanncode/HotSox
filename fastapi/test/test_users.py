import os
import pytest
from unittest import mock
from fastapi.testclient import TestClient
from fastapi import Depends, UploadFile

from sqlalchemy.orm import Session
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql.base import PGDDLCompiler


# setup a test database for the test
from api.authentication.hashing import Hash
from api.database.models import User, Sock
from api.database.setup import Base, engine, SessionLocal

Base.metadata.create_all(bind=engine)

# import main fast api app for testing
from main import app, get_db


@compiles(DropTable, "postgresql")
def _compile_drop_table(element: DropTable, compiler: PGDDLCompiler, **kwargs) -> str:
    return compiler.visit_drop_table(element) + " CASCADE"


# build test client
client = TestClient(app)

# API Prefix for routes
PREFIX = os.environ.get("API_URL", "/api")

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
}


@pytest.fixture()
def test_db_setup():
    Base.metadata.create_all(bind=engine)

    # creat admin user
    response = client.post(
        PREFIX + "/user/",
        json=TEST_USER1,
    )
    response = client.post(
        PREFIX + "/user/",
        json=TEST_USER2,
    )
    # assert response.status_code == 200
    data = response.json()
    # assert "id" in data
    try:
        yield data
        Base.metadata.drop_all(bind=engine)
    except:
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def mock_upload_file():
    with mock.patch("builtins.open", mock.mock_open(read_data=b"test data")) as mocked:
        yield mocked


def login(username: str, password: str) -> dict:
    response = client.post(
        PREFIX + "/login/",
        data={"username": username, "password": password},
    )
    token = response.json().get("access_token", None)
    headers = {"Authorization": f"Bearer {token}"}
    return headers


def test_show_users_login_incorrect_cedentials(test_db_setup):
    response = client.get(PREFIX + "/users/")
    assert response.status_code == 401


def test_show_users_login_correct_cedentials(test_db_setup):
    response = client.get(PREFIX + "/users/", headers=login("admin", "admin"))
    assert response.status_code == 200


def test_show_user_admin(test_db_setup):
    response = client.get(PREFIX + "/user/admin", headers=login("admin", "admin"))
    assert response.status_code == 200
    # check for correct user
    with Session(engine) as db:
        db_user = db.query(User).filter(User.username == "admin").first()
        assert db_user
        for key in TEST_USER1.keys():
            if key != "password":
                assert key in db_user.__dict__.keys()


def test_show_user_that_do_not_exist(test_db_setup):
    response = client.get(PREFIX + "/user/DoNotExist", headers=login("admin", "admin"))
    assert response.status_code == 404
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
        PREFIX + "/user/admin", json=update_data, headers=login("admin", "admin")
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
        PREFIX + "/user/DoNotExist", json=update_data, headers=login("admin", "admin")
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


def test_delete_user(test_db_setup):
    username = "testuser2"
    email = "testuser2@testuser2.com"

    response = client.request(
        "DELETE",
        PREFIX + "/user",
        json={"username": username, "email": email},
        headers=login("admin", "admin"),
    )
    assert response.status_code == 204
    # check if element done not exists in the database
    with Session(engine) as db:
        db_user = db.query(User).filter(User.username == username).first()
        assert db_user == None


def test_delete_noneexisting_user(test_db_setup):
    response = client.request(
        "DELETE",
        PREFIX + "/user",
        json={"username": "DoNotExist", "email": "DoNotExist@DoNotExist.com"},
        headers=login("admin", "admin"),
    )
    assert response.status_code == 404


@mock.patch("api.controller.ctr_user.uploader.upload")
def test_user_upload_profilepic(mock_uploader_upload, test_db_setup):

    with Session(engine) as db:

        username = TEST_USER2["username"]
        password = TEST_USER2["password"]

        # set up the mock return value
        mock_uploader_upload.return_value = {
            "url": "https://cloudinary.com/mock_image.jpg"
        }

        # make a test user
        db_user = db.query(User).filter(User.username == username).first()

        # send a request to add a profile picture
        with open("./requirements.txt", "rb") as mock_file:
            response = client.post(
                f"{PREFIX}/user/{db_user.username}/profilepic",
                files={"file": ("filename", mock_file)},
                headers=login(username=username, password=password),
            )

        # check that the response is what we expect
        assert response.status_code == 201
        assert (
            response.json()["profile_picture"]
            == "https://cloudinary.com/mock_image.jpg"
        )

        # check that the user in the database has the new profile picture
        db_user = db.query(User).filter(User.username == username).first()
        assert len(db_user.profile_pictures) == 1
        assert (
            db_user.profile_pictures[0].profile_picture
            == "https://cloudinary.com/mock_image.jpg"
        )


@mock.patch("api.controller.ctr_user.uploader.upload")
def test_user_delete_profilepic(mock_uploader_upload, test_db_setup):

    with Session(engine) as db:

        username = TEST_USER2["username"]
        password = TEST_USER2["password"]

        # set up the mock return value
        mock_uploader_upload.return_value = {
            "url": "https://cloudinary.com/mock_image.jpg"
        }

        # make a test user
        db_user = db.query(User).filter(User.username == username).first()

        # send a request to add a profile picture
        with open("./requirements.txt", "rb") as mock_file:
            response = client.post(
                f"{PREFIX}/user/{db_user.username}/profilepic",
                files={"file": ("filename", mock_file)},
                headers=login(username=username, password=password),
            )

        # make a test user and get all pictures
        db_user = db.query(User).filter(User.username == TEST_USER2["username"]).first()
        before_delete_profilepics = db_user.profile_pictures

        # send a request to delete a profile picture
        response = client.request(
            "DELETE",
            f"{PREFIX}/user/{TEST_USER2['username']}/profilepic/{before_delete_profilepics[0].id}",
            json={"username": TEST_USER2["username"], "email": TEST_USER2["email"]},
            headers=login(TEST_USER2["username"], TEST_USER2["password"]),
        )

        # check that the response is what is expect
        assert response.status_code == 204

    # new session to persist changes of transactions before!
    with Session(engine) as db:
        # check that the user in the database has the new profile picture
        db_user_new = (
            db.query(User).filter(User.username == TEST_USER2["username"]).first()
        )
        assert len(db_user_new.profile_pictures) == len(before_delete_profilepics) - 1
