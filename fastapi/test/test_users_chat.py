from unittest import mock
from fastapi.testclient import TestClient

from sqlalchemy.orm import Session

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


def test_user_chats_no_chats(test_db_setup):
    response = client.get(
        PREFIX + f"/user/chats",
        headers=token("admin", "admin"),
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No chats available for user <admin>"}


def test_user_chats_with_chats(test_db_setup):

    with Session(engine) as db:
        user1 = db.query(User).filter(User.username == TEST_USER1["username"]).first()
        user2 = db.query(User).filter(User.username == TEST_USER2["username"]).first()

        # create a chat between two users
        db.add(MessageChat(user_id=user1.id, other_id=user2.id, message="test message"))
        db.commit()

    response = client.get(
        PREFIX + f"/user/chats",
        headers=token("admin", "admin"),
    )
    assert response.status_code == 200
    assert response.json()[0]["receiver"] == {
        "username": "testuser2",
        "email": "testuser2@testuser2.com",
    }
    assert response.json()[0]["message"] == "test message"
    assert response.json()[0]["seen_date"] == None
    assert response.json()[0]["sender"] == {
        "username": "admin",
        "email": "admin@admin.com",
    }


def test_user_chats_no_chats_between_users(test_db_setup):
    response = client.get(
        PREFIX + f"/user/chat/{TEST_USER2['username']}",
        headers=token("admin", "admin"),
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"No chats available between user <{TEST_USER1['username']}> and <{TEST_USER2['username']}>"
    }


def test_user_chats_with_chats_between_users(test_db_setup):

    with Session(engine) as db:
        user1 = db.query(User).filter(User.username == TEST_USER1["username"]).first()
        user2 = db.query(User).filter(User.username == TEST_USER2["username"]).first()
        # create a chat between two users
        db.add(MessageChat(user_id=user1.id, other_id=user2.id, message="test message"))
        db.commit()

    response = client.get(
        PREFIX + f"/user/chat/{TEST_USER2['username']}",
        headers=token("admin", "admin"),
    )
    assert response.status_code == 200
    assert response.json()[0]["receiver"] == {
        "username": "testuser2",
        "email": "testuser2@testuser2.com",
    }
    assert response.json()[0]["message"] == "test message"
    assert response.json()[0]["seen_date"] == None
    assert response.json()[0]["sender"] == {
        "username": "admin",
        "email": "admin@admin.com",
    }
