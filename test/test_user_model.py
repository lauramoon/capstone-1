"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from models.user import db, User
from sqlalchemy.exc import IntegrityError

# set an environmental variable to use a different database for tests 

os.environ['DATABASE_URL'] = "postgresql:///plant_quizzes_test"


# import app

from app import app

# Create tables once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

# Data for creating user

USER_DATA = {
    "username": "testuser",
    "password": "HASHED_PASSWORD"
}

class UserModelTestCase(TestCase):
    """Test user model."""

    def setUp(self):
        """Clear any errors, clear tables, create test client."""

        db.session.rollback()
        User.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(**USER_DATA)

        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.username, 'testuser')
        self.assertEqual(u.password, 'HASHED_PASSWORD')
        self.assertEqual(len(u.quizzes), 0)
        self.assertEqual(len(u.attempts), 0)
        self.assertEqual(repr(u), f"<User #{u.id}: testuser>")

    def test_user_signup_valid(self):
        """Does the signup function work with valid credentials?"""

        u = User.signup('signup_test', 'password')
        db.session.commit()

        self.assertEqual(u.username, 'signup_test')
        self.assertEqual(len(u.quizzes), 0)
        self.assertEqual(len(u.attempts), 0)
        self.assertEqual(repr(u), f"<User #{u.id}: signup_test>")

    def test_user_signup_missing(self):
        """Does the signup fail with required field missing?"""

        with self.assertRaises(ValueError):
            u = User.signup('signup_test', '')

    def test_user_signup_duplicate_username(self):
        """Does the signup fail with non-unique username?"""

        u = User(**USER_DATA)
        db.session.add(u)
        db.session.commit()

        with self.assertRaises(IntegrityError):
            u1 = User.signup('testuser', 'password')
            db.session.commit()

    def test_user_authenticate_valid(self):
        """Does authenticate work with valid credentials"""

        # Need to have real hashed and salted password in database
        u = User.signup('auth_test', 'password')
        db.session.add(u)
        db.session.commit()

        u1 = User.authenticate('auth_test', 'password')

        self.assertEqual(u1.username, 'auth_test')
        self.assertEqual(repr(u), f"<User #{u.id}: auth_test>")

    def test_user_authenticate_invalid_username(self):
        """Does authenticate fail with invalid username"""

        u = User.authenticate('auth_test_no', 'password')

        self.assertFalse(u)

    def test_user_authenticate_invalid_password(self):
        """Does authenticate fail with invalid password"""

        # Need to have real hashed and salted password in database
        u = User.signup('auth_test', 'password')
        db.session.add(u)
        db.session.commit()

        u1 = User.authenticate('auth_test', 'passwordy')

        self.assertFalse(u1)