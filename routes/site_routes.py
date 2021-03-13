"""General website routes"""

from flask import render_template
from app import app
from models.quiz import Quiz


@app.route('/')
def show_homepage():
    """Show homepage with links to quizzes available to anyone"""

    quizzes = Quiz.query.order_by(Quiz.id).limit(5).all()
    return render_template('index.html', quizzes=quizzes)


@app.route('/about')
def about_page():
    """Return about page"""

    return render_template('about.html')