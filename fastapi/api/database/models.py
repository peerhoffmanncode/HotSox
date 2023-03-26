from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    Float,
    String,
    DateTime,
    Date,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from cloudinary import uploader
from .setup import Base
from datetime import datetime


class User(Base):
    __tablename__ = "app_users_user"
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String)
    last_login = Column(DateTime, default=datetime.utcnow)
    is_superuser = Column(Boolean, default=False)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime, default=datetime.utcnow)
    info_about = Column(String)
    info_birthday = Column(Date, default=datetime.utcnow)
    info_gender = Column(Integer)
    location_city = Column(String)
    location_latitude = Column(Float)
    location_longitude = Column(Float)
    notification = Column(Boolean, default=True)
    social_instagram = Column(String)
    social_facebook = Column(String)
    social_twitter = Column(String)
    social_spotify = Column(String)

    profile_pictures = relationship(
        "UserProfilePicture",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    socks = relationship(
        "Sock",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    user_matches = relationship(
        "UserMatch",
        back_populates="user",
        foreign_keys="UserMatch.user_id",
        cascade="all, delete-orphan",
    )
    mail = relationship(
        "MessageMail",
        back_populates="user",
        foreign_keys="MessageMail.user_id",
        passive_deletes=True,
        cascade="all, delete-orphan",
    )
    chat = relationship(
        "MessageChat",
        back_populates="user",
        foreign_keys="MessageChat.user_id",
        cascade="all, delete-orphan",
    )

    # adminlog = relationship(
    #     "AdminLog",
    #     back_populates="user",
    #     foreign_keys="AdminLog.user_id",
    #     cascade="all, delete-orphan",
    # )

    # account_emailaddress = relationship(
    #     "AccountEmailaddress",
    #     back_populates="user",
    #     foreign_keys="AccountEmailaddress.user_id",
    #     cascade="all, delete-orphan",
    # )

    # socialaccount_socialaccount = relationship(
    #     "SocialaccountSocialaccount",
    #     back_populates="user",
    #     foreign_keys="SocialaccountSocialaccount.user_id",
    #     cascade="all, delete-orphan",
    # )

    def delete(self, db):
        """
        Function to fix buggy SQLAlchemy cascade deletion!
        """
        # find all matches and delete them
        matches = (
            db.query(UserMatch)
            .filter((UserMatch.user_id == self.id) | (UserMatch.other_id == self.id))
            .all()
        )
        [db.delete(match) for match in matches]

        # find all profilepic and delete them
        pictures = (
            db.query(UserProfilePicture)
            .filter(UserProfilePicture.user_id == self.id)
            .all()
        )
        # call delete method to ensure picture deletion from cloud storage
        [pic.delete(db) for pic in pictures]

        # find all chats and delete them
        chats = (
            db.query(MessageChat)
            .filter(
                (MessageChat.user_id == self.id) | (MessageChat.other_id == self.id)
            )
            .all()
        )
        [db.delete(chat) for chat in chats]

        # find all mails and delete it
        mails = db.query(MessageMail).filter(MessageMail.user_id == self.id).all()
        [db.delete(mail) for mail in mails]

        # find all socks and delete them
        socks = db.query(Sock).filter(Sock.user_id == self.id).all()
        [sock.delete(db) for sock in socks]

        # delete user
        db.delete(self)
        return


class UserProfilePicture(Base):
    __tablename__ = "app_users_userprofilepicture"

    id = Column(Integer, primary_key=True, index=True)
    profile_picture = Column(String)
    user_id = Column(
        Integer,
        ForeignKey("app_users_user.id", ondelete="CASCADE"),
    )

    user = relationship(
        "User",
        back_populates="profile_pictures",
    )

    def delete(self, db):
        """Function to delete a UserProfilePicture from cloudinary"""
        # generate public_id
        public_id = self.profile_picture.split("/")[-1]
        public_id = public_id[: public_id.find(".")]
        if public_id:
            uploader.destroy(public_id)
        db.delete(self)


class UserMatch(Base):
    __tablename__ = "app_users_usermatch"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("app_users_user.id", ondelete="CASCADE"),
        nullable=True,
    )
    other_id = Column(
        Integer,
        ForeignKey("app_users_user.id", ondelete="CASCADE"),
        nullable=True,
    )
    unmatched = Column(Boolean)
    chatroom_uuid = Column(UUID(as_uuid=True))

    user = relationship(
        "User",
        back_populates="user_matches",
        foreign_keys=[user_id],
    )
    other = relationship(
        "User",
        back_populates="user_matches",
        foreign_keys=[other_id],
    )


class Sock(Base):
    __tablename__ = "app_users_sock"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("app_users_user.id", ondelete="CASCADE"),
    )
    info_joining_date = Column(DateTime)
    info_name = Column(String)
    info_about = Column(String)
    info_color = Column(Integer)
    info_fabric = Column(Integer)
    info_fabric_thickness = Column(Integer)
    info_brand = Column(Integer)
    info_type = Column(Integer)
    info_size = Column(Integer)
    info_age = Column(Integer)
    info_separation_date = Column(Date)
    info_condition = Column(Integer)
    info_holes = Column(Integer)
    info_kilometers = Column(Integer)
    info_inoutdoor = Column(Integer)
    info_washed = Column(Integer)
    info_special = Column(String)

    user = relationship("User", back_populates="socks")
    profile_pictures = relationship(
        "SockProfilePicture",
        back_populates="sock",
        cascade="all, delete-orphan",
    )
    sock_likes = relationship(
        "SockLike",
        back_populates="sock",
        foreign_keys="SockLike.sock_id",
        cascade="all, delete-orphan",
    )

    def delete(self, db):
        """
        Function to fix buggy SQLAlchemy cascade deletion!
        """
        # find all likes and delete them
        likes = (
            db.query(SockLike)
            .filter(
                (SockLike.sock_id == self.id)
                | (SockLike.like_id == self.id)
                | (SockLike.dislike_id == self.id)
            )
            .all()
        )
        [db.delete(like) for like in likes]

        # find all profilepic and delete them
        pictures = (
            db.query(SockProfilePicture)
            .filter(SockProfilePicture.sock_id == self.id)
            .all()
        )
        [pic.delete(db) for pic in pictures]

        # delete sock
        db.delete(self)
        return


class SockProfilePicture(Base):
    __tablename__ = "app_users_sockprofilepicture"

    id = Column(Integer, primary_key=True, index=True)
    profile_picture = Column(String)
    sock_id = Column(
        Integer,
        ForeignKey("app_users_sock.id", ondelete="CASCADE"),
    )

    sock = relationship(
        "Sock",
        back_populates="profile_pictures",
    )

    def delete(self, db):
        """Function to delete a UserProfilePicture from cloudinary"""
        # generate public_id
        public_id = self.profile_picture.split("/")[-1]
        public_id = public_id[: public_id.find(".")]
        if public_id:
            uploader.destroy(public_id)
        db.delete(self)


class SockLike(Base):
    __tablename__ = "app_users_socklike"

    id = Column(Integer, primary_key=True, index=True)
    sock_id = Column(
        Integer,
        ForeignKey("app_users_sock.id", ondelete="CASCADE"),
    )
    like_id = Column(
        Integer,
        ForeignKey("app_users_sock.id", ondelete="CASCADE"),
        nullable=True,
    )
    dislike_id = Column(
        Integer,
        ForeignKey("app_users_sock.id", ondelete="CASCADE"),
        nullable=True,
    )

    sock = relationship(
        "Sock",
        back_populates="sock_likes",
        foreign_keys=[sock_id],
    )
    like = relationship(
        "Sock",
        back_populates="sock_likes",
        foreign_keys=[like_id],
    )
    dislike = relationship(
        "Sock",
        back_populates="sock_likes",
        foreign_keys=[dislike_id],
    )


class MessageMail(Base):
    __tablename__ = "app_users_messagemail"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("app_users_user.id", ondelete="CASCADE"),
    )
    subject = Column(String)
    content = Column(String)
    sent_date = Column(Date, default=datetime.utcnow)

    user = relationship(
        "User",
        back_populates="mail",
    )


class MessageChat(Base):
    __tablename__ = "app_users_messagechat"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("app_users_user.id", ondelete="CASCADE"),
    )
    other_id = Column(
        Integer,
        ForeignKey("app_users_user.id", ondelete="CASCADE"),
    )
    message = Column(String)
    sent_date = Column(DateTime)
    seen_date = Column(DateTime)

    user = relationship(
        "User",
        back_populates="chat",
        foreign_keys=[user_id],
    )
    other = relationship(
        "User",
        back_populates="chat",
        foreign_keys=[other_id],
    )


# class AdminLog(Base):
#     __tablename__ = "django_admin_log"
#     id = Column(Integer, primary_key=True, index=True)
#     action_time = Column(DateTime)
#     object_id = Column(Integer)
#     object_repr = Column(String)
#     action_flag = Column(Integer)
#     change_message = Column(String)
#     content_type_id = Column(Integer)
#     user_id = Column(
#         Integer,
#         ForeignKey("app_users_user.id", ondelete="CASCADE"),
#     )

#     user = relationship(
#         "User",
#         back_populates="adminlog",
#     )


# class AccountEmailaddress(Base):
#     __tablename__ = "account_emailaddress"
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String)
#     verified = Column(Boolean)
#     primary = Column(Boolean)
#     user_id = Column(
#         Integer,
#         ForeignKey("app_users_user.id", ondelete="CASCADE"),
#     )

#     user = relationship(
#         "User",
#         back_populates="account_emailaddress",
#     )


# class SocialaccountSocialaccount(Base):
#     __tablename__ = "socialaccount_socialaccount"
#     id = Column(Integer, primary_key=True, index=True)
#     provider = Column(String)
#     uid = Column(Integer)
#     last_login = Column(DateTime)
#     date_joined = Column(DateTime)
#     extra_data = Column(String)

#     user_id = Column(
#         Integer,
#         ForeignKey("app_users_user.id", ondelete="CASCADE"),
#     )

#     user = relationship(
#         "User",
#         back_populates="socialaccount_socialaccount",
#     )
