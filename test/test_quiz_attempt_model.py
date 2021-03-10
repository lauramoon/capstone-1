"""QuizAttempt model tests."""

# run these tests like:
#
#    python -m unittest test_quiz_attempt_model.py

import os
from unittest import TestCase
from models.user import db, User
from models.quiz_models import Quiz, Question
from models.quiz_attempt_models import QuestionAttempt, QuizAttempt
from add_questions import add_questions

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

class QuizAttemptModelTestCase(TestCase):
    """Test quiz_attempt model."""

    def setUp(self):
        """Clear any errors, clear tables, add test quizzes and user, create test client."""

        db.session.rollback()
        User.query.delete()
        Quiz.query.delete()
        Question.query.delete()

        add_questions('test/test_quiz_questions.csv', 'test family')

        u=User(**USER_DATA)
        db.session.add(u)
        db.session.commit()

        self.client = app.test_client()

    def test_quiz_attempt_model(self):
        """Test basic quiz_attempt model"""

        qa = QuizAttempt(quiz_id=Quiz.query.first().id, user_id=User.query.first().id)
        db.session.add(qa)
        db.session.commit()

        self.assertEqual(len(qa.questions), 0)
        self.assertEqual(qa.taken_by.username, 'testuser')
        self.assertEqual(qa.quiz, Quiz.query.first())
        self.assertTrue(qa.timestamp)


    def test_question_attempt_model(self):
        """Test basic question attempt model"""

        q = Quiz.query.first()
        qa = QuizAttempt(quiz_id=q.id, user_id=User.query.first().id)
        db.session.add(qa)

        score = 0
        for i in range(10):
            question_a = QuestionAttempt(question_id=q.questions[i].id, 
                            quiz_attempt_id=qa.id, 
                            answer_given='Giant rhubarb',
                            correct=q.questions[i].correct_answer == 'Giant rhubarb')
            if q.questions[i].correct_answer == 'Giant rhubarb':
                score += 1
            qa.questions.append(question_a)
        db.session.commit()

        qaq = qa.questions[0]
        u = User.query.one()

        self.assertEqual(len(qa.questions), 10)
        self.assertEqual(qaq.answer_given, 'Giant rhubarb')
        self.assertEqual(qaq.correct, False)
        self.assertEqual(score, 1)
        self.assertEqual(len(QuestionAttempt.query.all()), 10)
        self.assertEqual(QuestionAttempt.query.all()[0].quiz_attempt_id, qa.id)
        self.assertEqual(len(u.attempts), 1)
        self.assertEqual(u.attempts[0].id, qa.id)
        self.assertEqual(len(u.quizzes), 1)
        self.assertEqual(u.quizzes[0].id, q.id)

