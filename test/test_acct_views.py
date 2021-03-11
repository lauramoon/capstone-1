"""Account View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_acct_views.py


import os
from unittest import TestCase
from models.model import db, connect_db
from models.user import User
from sqlalchemy.exc import IntegrityError, InvalidRequestError


# set an environmental variable to use a different database for tests 

os.environ['DATABASE_URL'] = "postgresql:///plant_quizzes_test"


# import app and disable debug toolbar

from app import app, CURR_USER_KEY
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create tables once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

# Data for creating second user

USER_DATA = {
    "username": "testuser",
    "password": "HASHED_PASSWORD"
}

USER_DATA_DUP = {
    "username": "setupuser",
    "password": "HASHED_PASSWORD"
}

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class AcctViewTestCase(TestCase):
    """Test views for user account routes."""

    def setUp(self):
        """Clear any errors, clear tables, add user, create test client."""

        db.session.rollback()
        User.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="setupuser",
                                    password="testuser")

        db.session.commit()

    def test_get_signup_form(self):
        """Test sign-up form"""

        with self.client as c:
            with c.session_transaction() as sess:
                if CURR_USER_KEY in sess:
                    del sess[CURR_USER_KEY]

            resp = c.get("/signup")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3>Create an account</h3>', html)
            self.assertIn('<button class="btn waves-effect waves-light">Sign me up!</button>', html)

    def test_add_user_success(self):
        """Test post valid data to signup form"""

        with self.client as c:
            with c.session_transaction() as sess:
                if CURR_USER_KEY in sess:
                    del sess[CURR_USER_KEY]

            resp = c.post("/signup", data=USER_DATA)

            self.assertEqual(resp.status_code, 302)

            users = User.query.all()
            self.assertEqual(len(users), 2)

    def test_add_user_success_redirect(self):
        """Test post valid data to signup form, follow redirect"""

        with self.client as c:
            with c.session_transaction() as sess:
                if CURR_USER_KEY in sess:
                    del sess[CURR_USER_KEY]

            resp = c.post("/signup", data=USER_DATA, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div class="chip alert-success z-depth-2">Welcome, testuser!</div>', html)
            self.assertIn('<a href="user/quizzes" class="waves-effect waves-light btn-large">Quiz Results</a>', html)
            self.assertNotIn('<a href="/signup" class="waves-effect waves-light btn-large">Sign Up</a>', html)

    def test_add_user_duplicate_username(self):
        """Test attempt to signup with duplicate username"""

        with self.client as c:
            with c.session_transaction() as sess:
                if CURR_USER_KEY in sess:
                    del sess[CURR_USER_KEY]

            with self.assertRaises(InvalidRequestError):

                resp = c.post("/signup", data=USER_DATA_DUP)
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn ('alert-danger z-depth-2">Username setupuser already taken</div>', html)

                users = User.query.all()
                self.assertEqual(len(users), 1)


    def test_login_form_get(self):
        """Test login form loads"""

        with self.client as c:
            resp = c.get("/login")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Sign In</h2>', html)
            self.assertIn('<button class="btn waves-effect waves-light">Log In</button>', html)
            
    def test_login_valid_credentials(self):
        """Test login post with valid credentials"""

        with self.client as c:
            resp = c.post("/login", data={ "username": "setupuser", "password": "testuser" })

            self.assertEqual(resp.status_code, 302)

    def test_login_valid_credentials_redirect(self):
        """Test login post with valid credentials, follow redirect"""

        with self.client as c:
            resp = c.post("/login", 
                          data={ "username": "setupuser", "password": "testuser" },
                          follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn ('<div class="chip alert-success z-depth-2">Welcome back, setupuser!</div>', html)
            self.assertIn('<a href="user/quizzes" class="waves-effect waves-light btn-large">Quiz Results</a>', html)
            self.assertNotIn('<a href="/signup" class="waves-effect waves-light btn-large">Sign Up</a>', html)


    def test_login_invalid_credentials(self):
        """Test login post with invalid credentials"""

        with self.client as c:
            resp = c.post("/login", data={ "username": "testuser", "password": "incorrect" })
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn ('alert-danger z-depth-2">Invalid credentials.</div>', html)
            self.assertIn('<h2>Sign In</h2>', html)
            self.assertIn('<button class="btn waves-effect waves-light">Log In</button>', html)


    def test_logout(self):
        """Test log out"""

        with self.client as c:

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get('/logout')

            self.assertEqual(resp.status_code, 302)


    def test_logout_redirect(self):
        """Test log out with redirect to login page"""

        with self.client as c:

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get('/logout', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn ('alert-success z-depth-2">You have successfully logged out.</div>', html)
            self.assertIn('<h2>Sign In</h2>', html)
            self.assertIn('<button class="btn waves-effect waves-light">Log In</button>', html)
