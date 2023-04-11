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

# Setup Cloudinary
import cloudinary

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
)


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
    "password": Hash.encrypt("admin"),
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
    "password": Hash.encrypt("testuser2"),
    "is_active": True,
    "is_superuser": False,
}


@pytest.fixture()
def test_db_setup():
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        # create db object
        new_user1 = User(**TEST_USER1)
        new_user2 = User(**TEST_USER2)
        # write to db / commit!
        db.add(new_user1)
        db.add(new_user2)
        db.commit()
        db.refresh(new_user1)
        db.refresh(new_user2)

    # # creat admin user
    # response = client.post(
    #     PREFIX + "/user/",
    #     json=TEST_USER1,
    # )
    # response = client.post(
    #     PREFIX + "/user/",
    #     json=TEST_USER2,
    # )

    try:
        yield
        Base.metadata.drop_all(bind=engine)
    except:
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def mock_upload_file():
    with mock.patch("builtins.open", mock.mock_open(read_data=b"test data")) as mocked:
        yield mocked


def token(username: str, password: str) -> dict:
    response = client.post(
        PREFIX + "/token/",
        data={"username": username, "password": password},
    )
    token = response.json().get("access_token", None)
    headers = {"Authorization": f"Bearer {token}"}
    return headers


def test_show_users_login_incorrect_cedentials(test_db_setup):
    response = client.get(PREFIX + "/users")
    assert response.status_code == 401


def test_show_users_login_correct_cedentials(test_db_setup):
    response = client.get(PREFIX + "/users", headers=token("admin", "admin"))
    assert response.status_code == 200


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


def test_delete_user(test_db_setup):
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


def test_delete_noneexisting_user(test_db_setup):
    response = client.request(
        "DELETE",
        PREFIX + "/user",
        headers=token("DoNotExist", "DoNotExist"),
    )
    assert response.status_code == 401


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
                f"{PREFIX}/user/profilepic/",
                files={"file": ("filename", mock_file)},
                headers=token(username="testuser2", password="testuser2"),
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


@mock.patch("api.database.models.uploader.destroy")
@mock.patch("api.controller.ctr_user.uploader.upload")
def test_user_delete_profilepic(
    mock_uploader_upload, mock_uploader_destroy, test_db_setup
):
    with Session(engine) as db:
        username = TEST_USER2["username"]
        password = TEST_USER2["password"]

        # set up the mock return value
        mock_uploader_upload.return_value = {
            "url": "https://cloudinary.com/mock_image.jpg"
        }
        mock_uploader_destroy.return_value = True

        # make a test user
        db_user = db.query(User).filter(User.username == username).first()

        # send a request to add a profile picture
        with open("./requirements.txt", "rb") as mock_file:
            response = client.post(
                f"{PREFIX}/user/profilepic",
                files={"file": ("filename", mock_file)},
                headers=token(username="testuser2", password="testuser2"),
            )

        # make a test user and get all pictures
        db_user = db.query(User).filter(User.username == TEST_USER2["username"]).first()
        before_delete_profilepics = db_user.profile_pictures

        # send a request to delete a profile picture
        response = client.request(
            "DELETE",
            f"{PREFIX}/user/profilepic/{before_delete_profilepics[0].id}",
            headers=token("testuser2", "testuser2"),
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


def test_user_mails_no_mails_in_db(test_db_setup):
    response = client.get(
        PREFIX + f"/user/mail",
        headers=token("admin", "admin"),
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No mail available for user <admin>"}


@mock.patch("api.controller.ctr_mail.celery_send_mail_to_user")
def test_user_mail_send(mock_send_message, test_db_setup):
    # setup mock
    mock_send_message.return_value = {
        "subject": "TestMailSubject",
        "content": "TestMailContent",
    }

    response = client.post(
        PREFIX + f"/user/mail",
        headers=token("admin", "admin"),
        json={
            "subject": "TestMailSubject",
            "content": "TestMailContent",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "email has been sent",
        "email": {
            "subject": "TestMailSubject",
            "content": "TestMailContent",
        },
    }

    # double check database feedback
    response = client.get(
        PREFIX + f"/user/mail",
        headers=token("admin", "admin"),
    )
    assert response.status_code == 200
    assert response.json()[0]["content"] == "TestMailContent"
    assert response.json()[0]["subject"] == "TestMailSubject"


def test_user_chats_no_chats(test_db_setup):
    response = client.get(
        PREFIX + f"/user/chats",
        headers=token("admin", "admin"),
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No chats available for user <admin>"}


def test_user_chats_no_chats_between_users(test_db_setup):
    response = client.get(
        PREFIX + f"/user/chat/{TEST_USER2['username']}",
        headers=token("admin", "admin"),
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"No chats available between user <{TEST_USER1['username']}> and <{TEST_USER2['username']}>"
    }
