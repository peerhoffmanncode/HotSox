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
    assert response.json()["items"][0]["content"] == "TestMailContent"
    assert response.json()["items"][0]["subject"] == "TestMailSubject"


@mock.patch("api.controller.ctr_mail.celery_send_mail_to_user")
def test_user_mail_delete(mock_send_message, test_db_setup):
    # setup db
    with Session(engine) as db:
        # get user
        user = db.query(User).filter(User.username == "admin").first()
        # create mail
        mail = MessageMail(
            user_id=user.id, subject="TestMailSubject", content="TestMailContent"
        )
        db.add(mail)
        db.commit()
        db.refresh(mail)

        # delete mail
        response = client.request(
            "DELETE",
            f"{PREFIX}/user/mail/{mail.id}",
            headers=token("admin", "admin"),
        )

        # get all remaining mails after delete
        mail = db.query(MessageMail).filter(MessageMail.user_id == user.id).all()

    assert response.status_code == 204
    assert mail == []
