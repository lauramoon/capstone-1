"""Routes other than user account routes"""

from functools import wraps
from flask import render_template, flash, redirect, session, g
from app import app, CURR_USER_KEY
from models.user import db, User
from models.quiz import Quiz
from forms import QuizCreationForm
from generator.generator import get_plant_info
import routes.route_helpers as r

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

    # Only logged-in users may access quizzes beyond the first 5 general qizzes
    if not g.user and (quiz.num_by_family > 5 or quiz.family != 'general'):
        flash("Please sign up or log in to access that quiz.", "danger")
        return redirect('/')

    form = r.create_quiz_form(quiz) 

    if form.validate_on_submit():

        results, score, message = r.get_quiz_results(quiz, form)

        return render_template(
            'results.html', 
            quiz=quiz, 
            results=results, 
            score=score, 
            message=message)

    return render_template('quiz.html', form=form, quiz=quiz)


@app.route('/plant/<slug>')
def plant_detail(slug):
    """Show details about plant. 
    Plant will be 'False' if API call fails. This is handled in the template."""

    plant = get_plant_info(slug)
    search_slug = slug.replace('-', '+')

    return render_template('plant_detail.html', 
                        plant=plant, 
                        search_slug=search_slug)


@app.route('/quiz/new', methods=["GET", "POST"])
@checkuser
def new_quiz():
    """Create new quiz, available to users who have taken enough quizzes."""

    if not g.user.is_new_quiz_eligible():
        num = g.user.num_quizzes_created*10 + 10 - len(g.user.quizzes)
        flash(f"Take {num} more quizzes to create new quiz.")
        return redirect('/')

    form = QuizCreationForm()

    if form.validate_on_submit():
        quiz = Quiz.create(form.family.data)

        if quiz:
            quiz.created_by = g.user.username
            db.session.commit()
            flash("Quiz successfully created!", "success")
            return redirect(f'/quiz/{quiz.id}')

        else:
            flash("Something went wrong. Please try again later.")

    return render_template('create_quiz.html', form=form)


@app.route('/quiz/all')
@checkuser
def all_quizzes():
    """Show all available quizzes grouped by quiz family if logged-in user."""

    return render_template('all_quizzes.html', quiz_families=r.get_quiz_families())


@app.route('/user/quizzes')
@checkuser
def user_quizzes():
    latest_attempts = r.get_latest_attempts()

    return render_template('user_quizzes.html', latest_attempts=latest_attempts)


@app.route('/user/plants')
@checkuser
def user_page_plants():
    """Return page with list of plants user has seen in quizzes"""
    plants = r.get_user_plants()

    return render_template('user_plants.html', plants=plants)


@app.route('/about')
def about_page():
    """Return about page"""

    return render_template('about.html')