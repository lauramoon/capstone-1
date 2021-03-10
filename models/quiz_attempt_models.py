from datetime import datetime

from models.user import db

class QuizAttempt(db.Model):
    """Quiz attemps by a user"""

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
        default=datetime.utcnow()
    )

    num_correct = db.Column(db.Integer)

    questions = db.relationship(
        "QuestionAttempt",
        backref='quiz_attempt'
    )

class QuestionAttempt(db.Model):
    """Map quiz attempt to questions, mark if correct"""

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