"""SQLAlchemy db connection for models."""

from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import backref

db = SQLAlchemy()

def connect_db(app):
    """Connect database to Flask app"""

    db.app = app
    db.init_app(app)