from csv import DictReader
from models.model import db
from app import app
from models.quiz import Question, Quiz

def add_questions(file_path, family):
    """Add new quizzes to existing database from CSV of questions"""
    
    with open(f'{file_path}', newline="") as csvfile:
        questions = DictReader(csvfile)
        count = 0
        for question in questions:
            if count % 10 == 0:
                new_quiz = Quiz(family=family, num_questions=10)
                db.session.add(new_quiz)
            new_question = Question(**question)
            new_quiz.questions.append(new_question)
            db.session.add(new_question)
            count += 1
        db.session.commit()

# add_questions('generator/pea_3.csv', 'Pea family')
