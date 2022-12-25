from django.test import TestCase

from .models import User
from django.utils import timezone
from datetime import date

# Create your tests here.
class UserModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create(
            username="test",
            first_name="test first",
            last_name="test last",
            email="test@mail.com",
            password="str0ng_pwd!",
            birthday=date(2000, 1, 1),
            user_sex="female",
            interested_sex="male",
        )

    def test_str_method(self):
        # Check that the __str__ method returns the expected string
        self.assertEqual(str(self.user), "[test] test first test last, Female")

    def test_is_18_years_method(self):
        # Check that the is_18_years method returns True for users over 18 years old
        self.assertTrue(self.user.is_18_years())
        # Create a test user who is 17 years old
        user_17_years = User.objects.create(
            username="test_17",
            first_name="test_17 first",
            last_name="test_17 last",
            email="test_17@mail.com",
            password="str0ng_pwd!",
            birthday=date(2005, 1, 1),
            user_sex="male",
            interested_sex="female",
        )
        # Check that the is_18_years method returns False for users under 18 years old
        self.assertFalse(user_17_years.is_18_years())

    def test_to_json_method(self):
        # Check that the to_json method returns a dictionary with the expected keys and values
        self.assertDictEqual(
            self.user.to_json(),
            {
                "pk": self.user.pk,
                "username": self.user.username,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email,
                "birthday": self.user.birthday,
                "user_sex": self.user.user_sex,
                "interested_sex": self.user.interested_sex,
                "last_login": self.user.last_login,
                "date_joined": self.user.date_joined,
                "is_active": self.user.is_active,
            },
        )
