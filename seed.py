"""Seed database with sample data from CSV Files."""

from csv import DictReader
from app import db
from models.quiz import Question, Quiz


db.drop_all()
db.create_all()

with open('generator/general_5.csv') as questions:
    db.session.bulk_insert_mappings(Question, DictReader(questions))

with open('generator/rose_3.csv') as questions:
    db.session.bulk_insert_mappings(Question, DictReader(questions))

with open('generator/aster_3.csv') as questions:
    db.session.bulk_insert_mappings(Question, DictReader(questions))

with open('generator/mint_3.csv') as questions:
    db.session.bulk_insert_mappings(Question, DictReader(questions))

with open('generator/pea_3.csv') as questions:
    db.session.bulk_insert_mappings(Question, DictReader(questions))

questions = Question.query.all()

family = ['general']*5 + ['Rose family']*3 + ['Aster family']*3
family = family + ['Mint family']*3 + ['Pea family']*3

for i in range(len(family)):
    new_quiz = Quiz(family=family[i], num_questions=10)
    for j in range(10):
        questions[10*i + j].family = family[i]
        new_quiz.questions.append(questions[i*10 + j])
    db.session.add(new_quiz)

db.session.commit()
