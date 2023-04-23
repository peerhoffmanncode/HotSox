from typing import List, Optional
from uuid import uuid4, UUID

from datetime import datetime, date
from pydantic import BaseModel, validator, Field, HttpUrl, EmailStr, AnyUrl


# basic schema for simplified user display
class SimplyUser(BaseModel):
    # id: int | None
    username: str | None
    email: EmailStr | None

    class Config:
        orm_mode = True


# basic schema for simplified sock display
class SimplySock(BaseModel):
    # id: int | None
    info_name: str | None
    info_special: str | None

    class Config:
        orm_mode = True


################################################################
### Actual HotSox models                                      ##
################################################################


# basic schema for simplified user display
class UserProfilePic(SimplyUser):
    profile_pic: str | None

    class Config:
        orm_mode = True


# basic schema for chats
class MessageChat(BaseModel):
    id: int | None
    other: Optional[SimplyUser | None] = Field(..., alias="receiver")
    message: str | None
    sent_date: datetime | None
    seen_date: datetime | None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class MessageChatWithSender(MessageChat):
    user: Optional[SimplyUser | None] = Field(..., alias="sender")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# basic schema for mails
class MessageMail(BaseModel):
    id: int | None
    subject: str | None
    content: str | None
    sent_date: datetime | date | None

    class Config:
        orm_mode = True


class MessageMail_with_id(MessageMail):
    id: int

    class Config:
        orm_mode = True


# basic schema for sending mails
class MessageMailSending(BaseModel):
    # id: int | None
    subject: str | None
    content: str | None

    class Config:
        orm_mode = True


# basic schema for likes/dislike of socks
class SockLikes(BaseModel):
    id: int | None
    sock: SimplySock | None
    like: SimplySock | None
    dislike: SimplySock | None

    class Config:
        orm_mode = True


# basic schema for sock profile pics
class SockProfilePicture(BaseModel):
    id: int | None
    profile_picture: str | None
    # sock_id: str | None

    class Config:
        orm_mode = True


# basic schema for socks
class ShowSock(BaseModel):
    id: int | None = Field(..., alias="id_sock")
    # user_id: int
    info_joining_date: date | None
    info_name: str | None
    info_about: str | None
    info_color: int | None = Field(1, ge=1, le=10)
    info_fabric: int | None = Field(1, ge=1, le=7)
    info_fabric_thickness: int | None = Field(1, ge=1, le=7)
    info_brand: int | None = Field(1, ge=1, le=13)
    info_type: int | None = Field(1, ge=1, le=9)
    info_size: int | None = Field(1, ge=1, le=7)
    info_age: int | None
    info_separation_date: date | None
    info_condition: int | None = Field(1, ge=1, le=12)
    info_holes: int | None
    info_kilometers: int | None
    info_inoutdoor: int | None = Field(1, ge=1, le=9)
    info_washed: int | None
    info_special: str | None
    profile_pictures: Optional[list[SockProfilePicture]]
    sock_likes: Optional[list[SockLikes]]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# basic schema for socks
class CreateUpdateSock(BaseModel):
    # id: int | None = Field(..., alias="id_sock")
    # user_id: int
    # info_joining_date: date | None
    info_name: str | None
    info_about: str | None
    info_color: int | None = Field(1, ge=1, le=10)
    info_fabric: int | None = Field(1, ge=1, le=7)
    info_fabric_thickness: int | None = Field(1, ge=1, le=7)
    info_brand: int | None = Field(1, ge=1, le=13)
    info_type: int | None = Field(1, ge=1, le=9)
    info_size: int | None = Field(1, ge=1, le=7)
    info_age: int | None
    info_separation_date: date | None
    info_condition: int | None = Field(1, ge=1, le=12)
    info_holes: int | None
    info_kilometers: int | None
    info_inoutdoor: int | None = Field(1, ge=1, le=9)
    info_washed: int | None
    info_special: str | None
    # profile_pictures: Optional[list[SockProfilePicture]]
    # sock_likes: Optional[list[SockLikes]]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# basic schema for user matches
class UserMatch(BaseModel):
    id: int | None
    # user: Optional[SimplyTheUser]
    other: Optional[SimplyUser | None] = Field(..., alias="matched_with")
    unmatched: bool | None
    chatroom_uuid: UUID | None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# basic schema for user profile pics
class UserProfilePicture(BaseModel):
    id: int | None
    profile_picture: str | None
    # user_id: str | None

    class Config:
        orm_mode = True


# basic schema for user
class ShowUser(BaseModel):
    id: int = Field(..., alias="id_user")
    username: str
    # password: str
    first_name: str
    last_name: str
    email: EmailStr
    last_login: Optional[datetime]
    is_superuser: bool
    is_staff: bool
    is_active: bool
    date_joined: Optional[datetime]
    info_about: Optional[str]
    info_birthday: Optional[date]
    info_gender: Optional[int | None]  # = Field(1, ge=1, le=8)
    location_city: Optional[str]
    location_latitude: Optional[float]
    location_longitude: Optional[float]
    notification: Optional[bool]
    social_instagram: Optional[str] = Field("https://www.instagram.com/")
    social_facebook: Optional[str] = Field("https://www.facebook.com/")
    social_twitter: Optional[str] = Field("https://twitter.com/")
    social_spotify: Optional[str] = Field("https://open.spotify.com/")
    profile_pictures: Optional[list[UserProfilePicture]]
    user_matches: Optional[list[UserMatch]]
    mail: Optional[list[MessageMail]]
    chat: Optional[list[MessageChat]]
    socks: Optional[list[ShowSock]]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# basic schema for user_edit
class EditUser(BaseModel):
    username: str | None
    first_name: str | None
    last_name: str | None
    email: EmailStr | None
    info_about: str | None
    info_birthday: date | None
    info_gender: int = Field(1, ge=1, le=8)
    location_city: str | None
    notification: bool | None
    social_instagram: Optional[str] = Field("https://www.instagram.com/")
    social_facebook: Optional[str] = Field("https://www.facebook.com/")
    social_twitter: Optional[str] = Field("https://twitter.com/")
    social_spotify: Optional[str] = Field("https://open.spotify.com/")

    class Config:
        orm_mode = True

    @validator("info_birthday")
    @classmethod
    def at_least_18years_oĺd(cls, value):
        if isinstance(value, date):
            difference = date.today() - value
            # Check if the difference is equal to or greater than 18 years(including leap)
            if round(difference.days / 365.2425, 2) < 18:
                # self.add_error('date_of_birth', 'Enter a valid date of birth')
                raise ValueError("You must be at least 18 years old!")
        return value


class EditUserOut(EditUser):
    location_latitude: float | None
    location_longitude: float | None

    class Config:
        orm_mode = True


class CreateUser(EditUser):
    password: str

    class Config:
        orm_mode = True


class CreateUserOut(EditUserOut):
    password: str

    class Config:
        orm_mode = True


# basic schema for login
class Login(BaseModel):
    username: str
    password: str


# basic schema for JWT Token
class Token(BaseModel):
    access_token: str
    token_type: str


# basic schema for JWT Token
class TokenData(BaseModel):
    username: Optional[str] = None
    superuser: Optional[bool] = False
    active: Optional[bool] = True
