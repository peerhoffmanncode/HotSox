import os
from dotenv import load_dotenv

load_dotenv("../.env")
if os.environ.get("SECRET_KEY", None) is None:
    print("can not find env file!")
    exit(-1)

from fastapi import FastAPI

# cloudinary
import cloudinary

# import Database setup
from api.database.setup import engine, get_db
from api.database import models

# import routers
from api.routers import auth, user, sock


# Setup Cloudinary
cloudinary.config(
    cloud_name=os.environ.get("cloudinary_cloud_name"),
    api_key=os.environ.get("cloudinary_api_key"),
    api_secret=os.environ.get("cloudinary_api_secret"),
)


# build FastAPI app / Hide schemas from docs
app = FastAPI(
    openapi_url=os.environ.get("API_URL", "/api") + "/openapi.json",
    docs_url=os.environ.get("API_URL", "/api") + "/docs",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

# setup SQLAlchemy database engine
# models.Base.metadata.create_all(engine)

# include API routs
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(sock.router)
