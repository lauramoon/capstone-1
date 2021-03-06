"""SQLAlchemy models for quiz and quiz questions"""

from datetime import datetime
from models.model import db
from models.quiz_attempt import QuestionAttempt
import sys
sys.path.append('../')
from generator.generator import create_quiz


def search_slug(context):
    """Turns the plant slug into a string suitable for Wikipedia or Google search"""

    return context.get_current_parameters()['slug'].replace('-', '+')


def num_by_family(context):
    """Gives number to quiz based on how many quizzes of the same family 
    are already in the database"""

    family = context.get_current_parameters()['family']
    return len(Quiz.query.filter(Quiz.family==family).all()) + 1


class Quiz(db.Model):
    """Quiz"""

    __tablename__ = 'quizzes'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    num_questions = db.Column(db.Integer)

    family = db.Column(
        db.Text, 
        nullable=False
    )

    num_by_family = db.Column(
        db.Integer,
        default=num_by_family
    )

    created_on = db.Column(
        db.DateTime,
        default = datetime.utcnow
    )

    created_by = db.Column(
        db.Text,
        default = 'system'
    )

    questions = db.relationship(
        'Question',
        secondary="quiz_questions",
        backref='part_of'
    )

    attempts = db.relationship(
        'QuizAttempt',
        backref='quiz'
    )

    @classmethod
    def create(cls, family):
        """Create new quiz from identified family.
        If error in quiz creation, return False"""

        questions = create_quiz(family)

        if not questions:
            return False

        quiz = Quiz(num_questions=10, family=family)
        db.session.add(quiz)
        db.session.commit()

        for question in questions:
            new_question = Question(**question)
            new_question.family = family
            db.session.add(new_question)
            db.session.commit()
            quiz.questions.append(new_question)

        db.session.commit()
        return quiz

class Question(db.Model):
    """Quiz question"""

    __tablename__ = 'questions'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    url = db.Column(
        db.Text
    )

    correct_answer = db.Column(
        db.Text
    )

    wrong_answer_1 = db.Column(
        db.Text
    )

    wrong_answer_2 = db.Column(
        db.Text
    )

    wrong_answer_3 = db.Column(
        db.Text
    )

    slug = db.Column(
        db.Text
    )

    search_slug = db.Column(
        db.Text,
        default=search_slug
    )

    attempts = db.relationship(
        'QuestionAttempt',
        backref='question'
    )
        

class QuizQuestion(db.Model):
    """Map quiz questions to a quiz"""

    __tablename__ = 'quiz_questions'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    question_id = db.Column(
        db.Integer,
        db.ForeignKey('questions.id', ondelete='cascade')
    )

    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey('quizzes.id', ondelete='cascade')
    )
