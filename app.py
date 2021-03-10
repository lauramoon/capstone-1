import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from models.user import db, connect_db


CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///plant_quizzes'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "plantsecretsaresecret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

import routes.acct_routes
import routes.other_routes
