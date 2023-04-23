import os
import pytest
from unittest import mock
from fastapi.testclient import TestClient

from sqlalchemy.orm import Session
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql.base import PGDDLCompiler

from api.authentication.hashing import Hash
from api.database.models import User
from api.database.setup import Base, engine

# import main fast api app for testing
from main import app


# build test client
client = TestClient(app)

# API Prefix for routes
PREFIX = os.environ.get("FASTAPI_URL", "/fastapi/v1")

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
    # hack to be able to drop all tables in postgresql CASCADE style
    @compiles(DropTable, "postgresql")
    def _compile_drop_table(
        element: DropTable, compiler: PGDDLCompiler, **kwargs
    ) -> str:
        return compiler.visit_drop_table(element) + " CASCADE"

    # clean all tables
    Base.metadata.drop_all(bind=engine)
    # create all tables
    Base.metadata.create_all(bind=engine)

    # setup database for tests
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

    try:
        # yield db to test as fixture
        yield
        # drop all tables after test
        Base.metadata.drop_all(bind=engine)
    except:
        # in case of error, drop all tables
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def mock_upload_file():
    # mock object for file open
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
