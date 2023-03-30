from passlib.context import CryptContext
from passlib.apps import django_context

# pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    """
    General class for hashing.

    using [django_context] give the ability to work with django
    hashed pwds from the existing database.
    """

    @staticmethod
    def encrypt(password: str) -> str:
        """set hashed pwd"""
        return django_context.hash(password)

    @staticmethod
    def verify(hashed_password, plain_password) -> bool:
        """
        check clean pwd against hashed one!
        return [bool]
        """
        return django_context.verify(plain_password, hashed_password)
