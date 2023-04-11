from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Setup Database credentials
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

# build database url string
if os.getenv("GITHUB_WORKFLOW"):
    # check if we are in GITHUB ACTION MODE ?
    DATABASE_URL = (
        "postgresql+psycopg2://postgres:postgres@localhost:5432/github-actions"
    )

else:
    # check if we have ENV Vars set e.g. env.py/Dockerfile/...?
    import sys

    if "test" in sys.argv[0] or "test" in sys.argv[1]:
        DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
    else:
        DATABASE_URL = (
            f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


def get_db():
    with SessionLocal() as db:
        yield db


def celery_db():
    return SessionLocal()
