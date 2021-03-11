"""Other view tests (not user-specific)."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_other_views.py


import os
from unittest import TestCase
from models.model import db, connect_db
from models.user import User
from models.quiz import Quiz
from add_questions import add_questions


# set an environmental variable to use a different database for tests 

os.environ['DATABASE_URL'] = "postgresql:///plant_quizzes_test"


# import app and disable debug toolbar

from app import app, CURR_USER_KEY
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create tables once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

# The form won't validate if each answer isn't one of the choices for that question

ANSWERS = { 'questions-0-answers': 'Garland spiraea',
            'questions-1-answers': 'Mountain hemlock',
            'questions-2-answers': 'Chinese giant-hyssop',
            'questions-3-answers': 'Giant rhubarb',
            'questions-4-answers': 'Glademallow',
            'questions-5-answers': 'Yellow colicroot',
            'questions-6-answers': 'Creeping sibbaldia',
            'questions-7-answers': 'Machete',
            'questions-8-answers': 'Bur chervil',
            'questions-9-answers': 'Longspur seablush'
          }

ANSWERS_INCOMPLETE = { 'questions': [{'answers': ''}]*10 }


class AcctViewTestCase(TestCase):
    """Test views other than user account views."""

    def setUp(self):
        """Clear any errors, clear tables, add user and 2 quizzes, create test client."""

        db.session.rollback()
        User.query.delete()
        Quiz.query.delete()

        self.testuser = User.signup(username="setupuser",
                                    password="testuser")

        add_questions('test/test_quiz_questions.csv', 'test family')

        db.session.commit()

        self.client = app.test_client()

    def test_home_logged_in(self):
        """Test home page with user logged in"""

        with self.client as c:

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="user/quizzes" class="waves-effect waves-light btn-large">Quiz Results</a>', html)
            self.assertNotIn('<a href="/signup" class="waves-effect waves-light btn-large">Sign Up</a>', html)

    def test_home_no_user(self):
        """Test home page with user logged out"""

        with self.client as c:

            with c.session_transaction() as sess:
                if CURR_USER_KEY in sess:
                    del sess[CURR_USER_KEY]

            resp = c.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('<a href="user/quizzes" class="waves-effect waves-light btn-large">Quiz Results</a>', html)
            self.assertIn('<a href="/signup" class="waves-effect waves-light btn-large">Sign Up</a>', html)


    def test_quiz_page(self):
        """Test quiz page"""

        with self.client as c:

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            q = Quiz.query.first()
            resp = c.get(f'/quiz/{q.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test Family Quiz 1</h1>', html)
            self.assertNotIn('<span class="red-text">answer is required</span>', html)
            self.assertIn('<span class="choice-span grey-text text-darken-2">', html)
            self.assertIn('waves-light quiz-submit">See results</button>', html)


    def test_quiz_page_no_user(self):
        """Test quiz page with no user logged in"""

        with self.client as c:

            with c.session_transaction() as sess:
                if CURR_USER_KEY in sess:
                    del sess[CURR_USER_KEY]

            q = Quiz.query.first()
            resp = c.get(f'/quiz/{q.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

    def test_quiz_page_no_user_redirect(self):
        """Test quiz page with no user logged in, follow redirect"""

        with self.client as c:

            with c.session_transaction() as sess:
                if CURR_USER_KEY in sess:
                    del sess[CURR_USER_KEY]

            q = Quiz.query.first()
            resp = c.get(f'/quiz/{q.id}', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn ('alert-danger z-depth-2">Please sign up or log in to access that quiz.</div>', html)
            self.assertNotIn('<a href="user/quizzes" class="waves-effect waves-light btn-large">Quiz Results</a>', html)
            self.assertIn('<a href="/signup" class="waves-effect waves-light btn-large">Sign Up</a>', html)


    def test_quiz_submit_incomplete(self):
        """Test submission of incomplete quiz"""

        with self.client as c:

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            q = Quiz.query.first()
            resp = c.post(f'/quiz/{q.id}', data=ANSWERS_INCOMPLETE)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test Family Quiz 1</h1>', html)
            self.assertIn('<span class="red-text">answers required</span>', html)
            self.assertIn('<span class="choice-span grey-text text-darken-2">', html)
            self.assertIn('waves-light quiz-submit">See results</button>', html)


    def test_quiz_submit(self):
        """Test submission of quiz with a valid set of answers"""

        with self.client as c:

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            quiz = Quiz.query.first()
            resp = c.post(f'/quiz/{quiz.id}', data=ANSWERS)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test Family Quiz 1</h1>', html)
            self.assertIn('amber-text text-darken-4">(you answered Bur chervil)</span>', html)
            self.assertIn('<h4>You got 1 of 10 answers correct!</h4>', html)
            self.assertIn('<a href="/plant/gunnera-manicata" class="btn', html)

    def test_plant_detail(self):
        """Test plant detail page"""

        with self.client as c:

            resp = c.get('/plant/gunnera-manicata')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Giant Rhubarb</h1>', html)
            self.assertIn('<h5>Where it grows: S. Brazil</h5>', html)
