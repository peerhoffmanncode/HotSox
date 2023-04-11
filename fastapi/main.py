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
from api.routers import auth, user, user_pic, user_mail, user_chat, sock, sock_pic


# Setup Cloudinary
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
)


# build FastAPI app / Hide schemas from docs
app = FastAPI(
    title="HotSox API",
    openapi_url=os.environ.get("API_URL", "/api") + "/openapi.json",
    docs_url=os.environ.get("API_URL", "/api") + "/docs",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

# setup SQLAlchemy database engine
# models.Base.metadata.create_all(engine)

# include API routs
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(user_pic.router)
app.include_router(user_mail.router)
app.include_router(user_chat.router)
app.include_router(sock.router)
app.include_router(sock_pic.router)
