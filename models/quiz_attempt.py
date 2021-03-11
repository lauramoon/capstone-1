"""Models for quiz attempts by a user with associated question attempts"""

from datetime import datetime

from models.model import db

class QuizAttempt(db.Model):
    """Quiz attempts by a user"""

    __tablename__ = 'quiz_attempts' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey('quizzes.id', ondelete='cascade')
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now()
    )

    num_correct = db.Column(db.Integer)

    questions = db.relationship(
        "QuestionAttempt",
        backref='quiz_attempt'
    )

class QuestionAttempt(db.Model):
    """Maps quiz attempt to quiz questions, mark if correct"""

    __tablename__ = 'question_attempts'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    question_id = db.Column(
        db.Integer,
        db.ForeignKey('questions.id', ondelete='cascade')
    )

    quiz_attempt_id = db.Column(
        db.Integer,
        db.ForeignKey('quiz_attempts.id', ondelete='cascade')
    )

    answer_given = db.Column(
        db.Text
    )

    correct = db.Column(
        db.Boolean
    )