"""Routes other than user account routes"""

from functools import wraps
from flask import render_template, flash, redirect, session, g
from app import app, CURR_USER_KEY
from models.user import db, User
from models.quiz_models import Quiz
from models.quiz_attempt_models import QuizAttempt
from forms import QuizForm
from generator.generator import get_plant_info
from routes.route_helpers import get_quiz_families, get_user_plants, get_latest_attempts, create_quiz_form, get_quiz_results

# All routes other than user account-related routes

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def checkuser(func):
    """Wrapper function checks if user logged in else redirects to home with flash warning"""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.user:
            flash("Access unauthorized.", "danger")
            return redirect("/")
        return func(*args, **kwargs)
    return wrapper


@app.route('/')
def show_homepage():
    """Show homepage with links to quizzes available to anyone"""

    quizzes = Quiz.query.order_by(Quiz.id).limit(5).all()
    return render_template('index.html', quizzes=quizzes)


@app.route('/quiz/<int:num>', methods=["GET", "POST"])
def show_quiz(num):
    """Return quiz with specified id"""

    quiz = Quiz.query.get_or_404(num)

    if not g.user and (quiz.num_by_family > 5 or quiz.family != 'general'):
        # Only logged-in users may access quizzes beyond the first 5 general qizzes
        flash("Please sign up or log in to access that quiz.", "danger")
        return redirect('/')

    form = create_quiz_form(quiz) 

    if form.validate_on_submit():

        results, score = get_quiz_results(quiz, form)

        return render_template('results.html', quiz=quiz, results=results, score=score)

    return render_template('quiz.html', form=form, quiz=quiz)


@app.route('/plant/<slug>')
def plant_detail(slug):
    """Show details about plant"""
    plant = get_plant_info(slug)
    search_slug = slug.replace('-', '+')
    return render_template('plant_detail.html', plant=plant, search_slug=search_slug)


@app.route('/quiz/new')
@checkuser
def new_quiz():
    """Create new quiz."""

    quiz = Quiz.create('general')
    return redirect(f'/quiz/{quiz.id}')


@app.route('/quiz/all')
@checkuser
def all_quizzes():
    """Show all available quizzes grouped by quiz family if logged-in user."""

    return render_template('all_quizzes.html', quiz_families=get_quiz_families())


@app.route('/user/quizzes')
@checkuser
def user_quizzes():
    latest_attempts = get_latest_attempts()

    return render_template('user_quizzes.html', latest_attempts=latest_attempts)


@app.route('/user/plants')
@checkuser
def user_page_plants():
    """Return page with list of plants user has seen in quizzes"""
    plants = get_user_plants()

    return render_template('user_plants.html', plants=plants)