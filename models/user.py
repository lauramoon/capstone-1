"""SQLAlchemy user model and db connection for PlantQuizzes."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref


bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect database to Flask app"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    quizzes = db.relationship(
        'Quiz',
        secondary="quiz_attempts",
        backref='taken_by'
    )

    attempts = db.relationship(
        'QuizAttempt', 
        backref='taken_by'
    )


    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"


    @classmethod
    def signup(cls, username, password):
        """Sign up user. Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd
        )

        db.session.add(user)
        db.session.commit()
        return user


    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
