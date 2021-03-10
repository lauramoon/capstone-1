from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.core import FieldList, FormField, RadioField
from wtforms.validators import DataRequired, Length

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class QuestionForm(FlaskForm):
    """Question Form."""
    answers = RadioField('Select from:', choices=[])


class QuizForm(FlaskForm):
    """Quiz form - simply 10 Questions."""
    questions = FieldList(FormField(QuestionForm), min_entries=10)