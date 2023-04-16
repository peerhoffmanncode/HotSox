from unittest import mock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
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


def test_show_all_socks_of_a_user_no_socks(test_db_setup):
    response = client.get(PREFIX + "/user/socks", headers=token("admin", "admin"))
    content = response.json()
    print(content)
    assert response.status_code == 404
    assert content == {"detail": "No sock available"}


def test_show_all_socks_of_a_user_with_socks(test_db_setup):
    with Session(engine) as db:
        db_user = db.query(User).filter(User.username == "admin").first()

        sock1 = Sock(
            user_id=db_user.id,
            info_joining_date=datetime.utcnow(),
            info_name="Sock1",
            info_about="This is a fake sock.",
            info_color=1,
            info_fabric=2,
            info_fabric_thickness=3,
            info_brand=4,
            info_type=5,
            info_size=6,
            info_age=7,
            info_separation_date=date.today(),
            info_condition=8,
            info_holes=9,
            info_kilometers=10,
            info_inoutdoor=9,
            info_washed=12,
            info_special="None",
        )

        sock2 = Sock(
            user_id=db_user.id,
            info_joining_date=datetime.utcnow(),
            info_name="Sock2",
            info_about="This is a fake sock2.",
            info_color=1,
            info_fabric=2,
            info_fabric_thickness=3,
            info_brand=4,
            info_type=5,
            info_size=6,
            info_age=7,
            info_separation_date=date.today(),
            info_condition=8,
            info_holes=9,
            info_kilometers=10,
            info_inoutdoor=9,
            info_washed=12,
            info_special="None",
        )
        db.add(sock1)
        db.add(sock2)
        db.commit()

    # check socks for current user (with socks!)
    response = client.get(PREFIX + "/user/socks", headers=token("admin", "admin"))
    content = response.json()
    assert response.status_code == 200
    assert len(content) == 2

    # check socks for other user (with no socks!)
    response = client.get(
        PREFIX + "/user/socks", headers=token("testuser2", "testuser2")
    )
    content = response.json()
    assert response.status_code == 404
    assert content == {"detail": "No sock available"}


def test_show_sock_of_a_user_no_sock(test_db_setup):
    response = client.get(PREFIX + "/user/sock/1", headers=token("admin", "admin"))
    content = response.json()
    print(content)
    assert response.status_code == 404
    assert content == {"detail": "Sock with the id 1 is not available"}


def test_show_sock_of_a_user_with_sock(test_db_setup):

    with Session(engine) as db:
        db_user = db.query(User).filter(User.username == "admin").first()

        sock1 = Sock(
            user_id=db_user.id,
            info_joining_date=datetime.utcnow(),
            info_name="Sock1",
            info_about="This is a fake sock.",
            info_color=1,
            info_fabric=2,
            info_fabric_thickness=3,
            info_brand=4,
            info_type=5,
            info_size=6,
            info_age=7,
            info_separation_date=date.today(),
            info_condition=8,
            info_holes=9,
            info_kilometers=10,
            info_inoutdoor=9,
            info_washed=12,
            info_special="None",
        )

        db.add(sock1)
        db.commit()
        db.refresh(sock1)

    response = client.get(
        PREFIX + f"/user/sock/{sock1.id}", headers=token("admin", "admin")
    )
    content = response.json()
    assert response.status_code == 200
    assert isinstance(content, dict)
    assert content["info_about"] == "This is a fake sock."
    assert content["info_age"] == 7
    assert content["info_brand"] == 4
    assert content["info_color"] == 1
    assert content["info_condition"] == 8
    assert content["info_fabric"] == 2
    assert content["info_fabric_thickness"] == 3
    assert content["info_holes"] == 9
    assert content["info_inoutdoor"] == 9
    assert content["info_kilometers"] == 10
    assert content["info_name"] == "Sock1"
    assert content["info_size"] == 6
    assert content["info_special"] == "None"
    assert content["info_type"] == 5
    assert content["info_washed"] == 12
    assert content["profile_pictures"] == []
    assert content["sock_likes"] == []


def test_update_sock_of_a_user_with_sock(test_db_setup):

    with Session(engine) as db:
        db_user = db.query(User).filter(User.username == "admin").first()

        sock1 = Sock(
            user_id=db_user.id,
            info_joining_date=datetime.utcnow(),
            info_name="Sock1",
            info_about="This is a fake sock.",
            info_color=1,
            info_fabric=2,
            info_fabric_thickness=3,
            info_brand=4,
            info_type=5,
            info_size=6,
            info_age=7,
            info_separation_date=date.today(),
            info_condition=8,
            info_holes=9,
            info_kilometers=10,
            info_inoutdoor=9,
            info_washed=12,
            info_special="None",
        )

        db.add(sock1)
        db.commit()
        db.refresh(sock1)

    update_data = {
        "info_name": "_update_Sock1",
        "info_about": "This is a updated fake sock.",
        "info_color": 1,
        "info_fabric": 1,
        "info_fabric_thickness": 1,
        "info_brand": 1,
        "info_type": 1,
        "info_size": 1,
        "info_age": 1,
        "info_separation_date": str(date.today() + timedelta(days=1)),
        "info_condition": 1,
        "info_holes": 1,
        "info_kilometers": 1,
        "info_inoutdoor": 1,
        "info_washed": 1,
        "info_special": "Update",
    }
    response = client.put(
        PREFIX + f"/user/sock/{sock1.id}",
        headers=token("admin", "admin"),
        json=update_data,
    )
    content = response.json()
    assert response.status_code == 202
    assert isinstance(content, dict)
    assert content["info_about"] == "This is a updated fake sock."
    assert content["info_age"] == 1
    assert content["info_brand"] == 1
    assert content["info_color"] == 1
    assert content["info_condition"] == 1
    assert content["info_fabric"] == 1
    assert content["info_fabric_thickness"] == 1
    assert content["info_holes"] == 1
    assert content["info_inoutdoor"] == 1
    assert content["info_kilometers"] == 1
    assert content["info_name"] == "_update_Sock1"
    assert content["info_separation_date"] == str(date.today() + timedelta(days=1))
    assert content["info_size"] == 1
    assert content["info_special"] == "Update"
    assert content["info_type"] == 1
    assert content["info_washed"] == 1
    assert content["profile_pictures"] == []
    assert content["sock_likes"] == []


def test_create_and_delete_sock_of_a_user(test_db_setup):

    with Session(engine) as db:
        db_user = db.query(User).filter(User.username == "admin").first()
        all_socks_before = db.query(Sock).filter(Sock.user_id == db_user.id).all()

    sock_data = {
        "info_name": "new_Sock3",
        "info_about": "This is a new fake sock.",
        "info_color": 1,
        "info_fabric": 1,
        "info_fabric_thickness": 1,
        "info_brand": 1,
        "info_type": 1,
        "info_size": 1,
        "info_age": 1,
        "info_separation_date": str(date.today() + timedelta(days=1)),
        "info_condition": 1,
        "info_holes": 1,
        "info_kilometers": 1,
        "info_inoutdoor": 1,
        "info_washed": 1,
        "info_special": "NEW!",
    }

    # create sock
    response = client.post(
        PREFIX + f"/user/sock",
        headers=token("admin", "admin"),
        json=sock_data,
    )
    # validate sock
    content = response.json()
    assert response.status_code == 201
    assert isinstance(content, dict)
    assert content["info_about"] == "This is a new fake sock."
    assert content["info_age"] == 1
    assert content["info_brand"] == 1
    assert content["info_color"] == 1
    assert content["info_condition"] == 1
    assert content["info_fabric"] == 1
    assert content["info_fabric_thickness"] == 1
    assert content["info_holes"] == 1
    assert content["info_inoutdoor"] == 1
    assert content["info_kilometers"] == 1
    assert content["info_name"] == "new_Sock3"
    assert content["info_separation_date"] == str(date.today() + timedelta(days=1))
    assert content["info_size"] == 1
    assert content["info_special"] == "NEW!"
    assert content["info_type"] == 1
    assert content["info_washed"] == 1
    assert content["profile_pictures"] == []
    assert content["sock_likes"] == []

    # delete sock
    with Session(engine) as db:
        db_user = db.query(User).filter(User.username == "admin").first()
        all_socks_after = db.query(Sock).filter(Sock.user_id == db_user.id).all()
        # check one more sock in the database for correct user
        assert len(all_socks_after) == len(all_socks_before) + 1

        response = client.delete(
            PREFIX + f"/user/sock/1",
            headers=token("admin", "admin"),
        )
        db_user = db.query(User).filter(User.username == "admin").first()
        all_socks_after = db.query(Sock).filter(Sock.user_id == db_user.id).all()
        # check one more sock in the database for correct user

    assert response.status_code == 204
    # check that created sock is deleted
    assert all_socks_after == all_socks_before
