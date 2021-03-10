"""Quiz model tests."""

# run these tests like:
#
#    python -m unittest test_quiz_model.py


import os
from unittest import TestCase
from models.user import db, User
from models.quiz_models import Quiz, Question
from add_questions import add_questions

# set an environmental variable to use a different database for tests 

os.environ['DATABASE_URL'] = "postgresql:///plant_quizzes_test"


# import app

from app import app

# Create tables once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

class QuizModelTestCase(TestCase):
    """Test quiz model."""

    def setUp(self):
        """Clear any errors, clear tables, add test quizzes, create test client."""

        db.session.rollback()
        User.query.delete()
        Quiz.query.delete()
        Question.query.delete()

        add_questions('test/test_quiz_questions.csv', 'test family')

        self.client = app.test_client()

    def test_quiz_model(self):
        """Test basic quiz model"""

        q = Quiz(num_questions=10, family='Test2 family')
        db.session.add(q)
        db.session.commit()

        self.assertEqual(len(q.questions), 0)
        self.assertEqual(q.num_questions, 10)
        self.assertEqual(q.family, 'Test2 family')
        self.assertEqual(len(Quiz.query.all()), 3)
        self.assertEqual(len(Quiz.query.filter(Quiz.family=='Test2 family').all()), 1)
        self.assertEqual(len(Quiz.query.filter(Quiz.family=='test family').all()), 2)
        self.assertEqual(q.num_by_family, 1)

    def test_question_model(self):
        """Test basic question model"""

        q = Quiz(num_questions=10, family='Test2 family')
        db.session.add(q)
        for i in range(10):
            question = Question(
                                url='test_url',
                                correct_answer='right answer',
                                wrong_answer_1='wrong one',
                                wrong_answer_2='wrong too',
                                wrong_answer_3='wrong 3',
                                slug='test-slug'
                                )
            q.questions.append(question)
        db.session.commit()

        qq = q.questions[0]

        self.assertEqual(len(q.questions), 10)
        self.assertEqual(qq.url, 'test_url')
        self.assertEqual(qq.correct_answer, 'right answer')
        self.assertEqual(qq.wrong_answer_2, 'wrong too')
        self.assertEqual(qq.search_slug, 'test+slug')
        self.assertEqual(len(Question.query.all()), 30)
        self.assertEqual(len(Question.query.filter(Question.url=='test_url').all()), 10)
        self.assertEqual(len(qq.part_of), 1)
        self.assertEqual(qq.part_of[0].id, q.id)

