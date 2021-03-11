"""Other view tests (not user-specific)."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_other_views.py


import os
from unittest import TestCase
from flask import appcontext_pushed, g
from models.model import db, connect_db
from models.user import User
from models.quiz import Quiz
from models.quiz_attempt import QuizAttempt, QuestionAttempt
from add_questions import add_questions
from routes.route_helpers import save_quiz_results


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


class UserViewTestCase(TestCase):
    """Test views other than user account views."""

    def setUp(self):
        """Clear any errors, clear tables, add user and 2 quizzes, 
        create test client."""

        db.session.rollback()
        User.query.delete()
        Quiz.query.delete()
        QuizAttempt.query.delete()

        self.testuser = User.signup(username="setupuser",
                                    password="testuser")
                                
        add_questions('test/test_quiz_questions.csv', 'test family')
        quiz = Quiz.query.first()

        attempt = QuizAttempt(user_id=self.testuser.id, quiz_id=quiz.id, num_correct=1)
        db.session.add(attempt)

        results = ['Giant rhubarb']*10

        for i in range(10):
            question_attempt = QuestionAttempt(question_id=quiz.questions[i].id, 
                            quiz_attempt_id=attempt.id, 
                            answer_given = results[i],
                            correct = quiz.questions[i].correct_answer == results[i])
            db.session.add(question_attempt)

        db.session.commit()

        self.client = app.test_client()


    def test_user_quizzes(self):
        """Test that quiz attempt reflected on user quizzes page"""

        with self.client as c:

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get('/user/quizzes')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<td><a href="/quiz/', html)
            self.assertIn('<td>1 of 10</td>', html)
            self.assertIn('href="/user/plants" class="btn-large waves-effect waves-light">', html)


    def test_user_plants(self):
        """Test that plant page shows the plants the user saw, not others"""

        with self.client as c:

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get('/user/plants')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>setupuser\'s Plants</h1>", html)
            self.assertIn('<a href="/plant/gunnera-manicata" class="btn', html)
            self.assertNotIn('<a href="/plant/vigna-radiata" class="btn', html)


    def test_quiz_list(self):
        """Test list of available quizzes"""

        with self.client as c:

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get('/quiz/all')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3>Test Family</h3>', html)
            self.assertIn('test family Quiz 2', html)
