"""Functions to process data for routes"""
import random
from flask import g
from models.user import db
from models.quiz_models import Quiz
from models.quiz_attempt_models import QuizAttempt, QuestionAttempt
from forms import QuizForm


def create_quiz_form(quiz):

    form = QuizForm()
    
    for i in range(10):
        form.questions[i].answers.choices = [
            quiz.questions[i].correct_answer,
            quiz.questions[i].wrong_answer_1,
            quiz.questions[i].wrong_answer_2,
            quiz.questions[i].wrong_answer_3
        ]
        random.shuffle(form.questions[i].answers.choices)
        form.questions[i].answers.label = quiz.questions[i].url
    
    return form


def get_quiz_results(quiz, form):
    """Take quiz form and pull out results, saving if user logged in"""
    results = []
    score = 0

    # Pull out results and score from form
    for i in range(10):
        answer = form.questions[i].answers.data
        correct = quiz.questions[i].correct_answer == answer
        results.append(answer)
        if correct:
            score += 1

    if g.user:
        save_quiz_results(results, score, quiz)

    return results, score


def save_quiz_results(results, score, quiz):
    """Save quiz results to database"""

    attempt = QuizAttempt(user_id=g.user.id, quiz_id=quiz.id)
    db.session.add(attempt)
    for i in range(10):
        question_attempt = QuestionAttempt(question_id=quiz.questions[i].id, 
                            quiz_attempt_id=attempt.id, 
                            answer_given = results[i],
                            correct = quiz.questions[i].correct_answer == results[i])
        db.session.add(question_attempt)
    
    attempt.num_correct = score
    db.session.commit()


def get_quiz_families():
    """Get quizzes grouped by plant family"""

    families = Quiz.query.with_entities(Quiz.family).group_by(Quiz.family)
    quiz_families = []
    for family in families:
        quiz_family = {}
        quiz_family['name'] = family[0]
        quiz_family['quizzes'] = Quiz.query.filter(Quiz.family==family[0])
        quiz_families.append(quiz_family)
    return quiz_families


def get_latest_attempts():
    """Get list of latest quiz attempts with associated data for each quiz"""

    latest_attempts = []
    for quiz in g.user.quizzes:
        attempt = {}
        attempt['quiz'] = quiz
        attempts = QuizAttempt.query.filter(
            QuizAttempt.quiz_id==quiz.id, 
            QuizAttempt.user_id==g.user.id
            ).order_by(QuizAttempt.timestamp.desc()).all()

        attempt['num_attempts'] = len(attempts)
        latest = attempts[0]
        attempt['latest'] = latest.num_correct
        attempt['timestamp'] = latest.timestamp
        total_correct = sum([att.num_correct for att in attempts])
        attempt['average'] = round(total_correct/len(attempts), 1)

        latest_attempts.append(attempt)

    return latest_attempts


def get_user_plants():
    """Get list of plants user has seen in quizzes"""
    plants = []
    user_quizzes = g.user.quizzes
    for quiz in user_quizzes:
        plants = plants + [question for question in quiz.questions]
    return list(dict.fromkeys(plants))