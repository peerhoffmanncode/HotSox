from unittest import mock
from fastapi.testclient import TestClient
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
import uuid
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
from api.database.models import User, Sock
from api.database.setup import engine


def create_test_records():
    sock_data = {
        "info_name": "Main Sock",
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
        "info_special": "main sock!",
    }
    # create sock
    response = client.post(
        PREFIX + f"/user/sock",
        headers=token("admin", "admin"),
        json=sock_data,
    )
    sock_data = {
        "info_name": "Test Sock1",
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
        "info_special": "Test sock!",
    }
    # create sock
    response = client.post(
        PREFIX + f"/user/sock",
        headers=token("testuser2", "testuser2"),
        json=sock_data,
    )
    sock_data = {
        "info_name": "Test Sock2",
        "info_about": "This is a new fake sock.",
        "info_color": 5,
        "info_fabric": 5,
        "info_fabric_thickness": 5,
        "info_brand": 5,
        "info_type": 5,
        "info_size": 5,
        "info_age": 5,
        "info_separation_date": str(date.today() - timedelta(days=365)),
        "info_condition": 5,
        "info_holes": 5,
        "info_kilometers": 5,
        "info_inoutdoor": 5,
        "info_washed": 5,
        "info_special": "Test sock2!",
    }
    # create sock
    response = client.post(
        PREFIX + f"/user/sock",
        headers=token("testuser2", "testuser2"),
        json=sock_data,
    )

    # send a request to add a profile picture
    with open("./requirements.txt", "rb") as mock_file:
        response = client.post(
            f"{PREFIX}/user/sock/1/profilepic",
            files={"file": ("filename", mock_file)},
            headers=token(username="admin", password="admin"),
        )
        assert response.status_code == 201

    # send a request to add a profile picture
    with open("./requirements.txt", "rb") as mock_file:
        response = client.post(
            f"{PREFIX}/user/sock/2/profilepic",
            files={"file": ("filename", mock_file)},
            headers=token(username="testuser2", password="testuser2"),
        )
        assert response.status_code == 201

        # send a request to add a profile picture
    with open("./requirements.txt", "rb") as mock_file:
        response = client.post(
            f"{PREFIX}/user/sock/3/profilepic",
            files={"file": ("filename", mock_file)},
            headers=token(username="testuser2", password="testuser2"),
        )
        assert response.status_code == 201

    with Session(engine) as db:
        username1 = TEST_USER1["username"]

        # setup user and sock base
        current_user = db.query(User).filter(User.username == username1).first()
        current_user_sock = (
            db.query(Sock).filter(Sock.user_id == current_user.id).first()
        )


@mock.patch("api.controller.ctr_sock_pic.uploader.upload")
def test_swipe_next_sock(mock_uploader_upload, test_db_setup):

    # set up the mock return value
    mock_uploader_upload.return_value = {"url": "https://cloudinary.com/mock_image.jpg"}

    create_test_records()

    response = client.get(
        PREFIX + f"/user/swipe/1/next",
        headers=token("admin", "admin"),
    )
    content = response.json()

    assert response.status_code == 200
    assert content["id_sock"] == 2


@mock.patch("api.controller.ctr_sock_pic.uploader.upload")
def test_swipe_judge_sock(mock_uploader_upload, test_db_setup):

    # set up the mock return value
    mock_uploader_upload.return_value = {"url": "https://cloudinary.com/mock_image.jpg"}

    # setup test data
    create_test_records()

    # judge first sock
    response = client.post(
        PREFIX + f"/user/swipe/1/judge/2?judgement=true",
        headers=token("admin", "admin"),
    )
    content = response.json()
    assert response.status_code == 200
    assert content == {"Message": "No new match found"}

    # judge second sock
    response = client.post(
        PREFIX + f"/user/swipe/1/judge/3?judgement=true",
        headers=token("admin", "admin"),
    )
    content = response.json()
    assert response.status_code == 200
    assert content == {"Message": "No new match found"}

    # judge first sock AGAIN!
    response = client.post(
        PREFIX + f"/user/swipe/1/judge/2?judgement=true",
        headers=token("admin", "admin"),
    )
    content = response.json()
    assert response.status_code == 404
    assert content == {"detail": "Sock with the id <2> was already judged!"}

    # other user judge first sock to get match!
    response = client.post(
        PREFIX + f"/user/swipe/2/judge/1?judgement=true",
        headers=token("testuser2", "testuser2"),
    )
    content = response.json()
    assert response.status_code == 200
    assert content["Message"] == "New match found"
    assert content["Match"]["user_id"] == 2
    assert content["Match"]["other_id"] == 1
    assert content["Match"]["chatroom_uuid"] != ""
    assert len(content["Match"]["chatroom_uuid"]) == 36
    assert content["Match"]["unmatched"] == False
