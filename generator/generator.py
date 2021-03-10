import requests
import random
import csv
import sys
sys.path.append('../')
import config

TOKEN = config.TREFLE_TOKEN
BASE_URL = f'https://trefle.io/api/v1/plants'


def create_quiz(family):
    plant_list = []
    answers = []

    family_url = get_url(family)

    page_range = get_range(family)

    for page in random.sample(range(1, page_range), 10):
        (more_answers, plant) = get_data(page, family_url)
        plant_list.append(plant)
        answers = answers + more_answers

    plants = [{'correct_answer': plant['common_name'], 
               'url': plant['image_url'], 
               'slug': plant['slug']} for plant in plant_list]
    
    wrong_answers = random.sample(answers, 30)

    for plant in plants:
        plant["wrong_answer_1"] = wrong_answers.pop()
        plant["wrong_answer_2"] = wrong_answers.pop()
        plant["wrong_answer_3"] = wrong_answers.pop()

    return plants


def get_data(page, family_url):
    plant_url = f'{family_url}&page={page}'

    try:
        raw_plant_list = requests.get(plant_url).json()

        clean_plant_list = clean(raw_plant_list["data"])

        common_names = [plant["common_name"] for plant in clean_plant_list]
        random_plant = random.choice(clean_plant_list)
        common_names.remove(random_plant["common_name"])

        return (common_names, random_plant)

    except:
        return False


def clean(plant_list):
    """Remove labeled images of dried plants. 
    Most of these have a URL containing the string below"""
    clean_list = []
    for plant in plant_list:
        url = plant["image_url"]
        if "d2seqvvyy3b8p2" not in url:
            clean_list.append(plant)
    return clean_list


def get_url(family):
    url = f'{BASE_URL}?token={TOKEN}&filter_not[common_name]=null&filter_not[image_url]=null'
    if family != 'general':
        url += f'&filter[family_common_name]={family}'
    return url


def get_range(family):
    if family == 'general':
        return 820
    else:
        return get_page_total(family)


def get_plant_info(slug):
    plant_url = f'{BASE_URL}/{slug}?token={TOKEN}'
    return requests.get(plant_url).json()["data"]
    

def get_page_total(family):
    plant_url = f'{BASE_URL}/?token={TOKEN}&filter_not[common_name]=null&filter_not[image_url]=null'
    try:
        explore = requests.get(plant_url + f'&filter[family_common_name]={family}').json()
        last_page = explore["links"]["last"].split('page=')[1]
        return int(last_page)
    except:
        return 0


def explore_families(family):
    plant_url = f'{BASE_URL}/?token={TOKEN}&filter_not[common_name]=null&filter_not[image_url]=null'
    print(plant_url)

    try:
        explore = requests.get(plant_url + f'&filter[family_common_name]={family}').json()
        print(f'meta: {explore["meta"]}')
        print(f'link-last: {explore["links"]["last"]}')
    except:
        print('Something went wrong')

def create_seed_quizzes(file_name, family, num):
    """Export to csv data for 'num' quizzes from given family to seed database."""

    with open(f'{file_name}.csv', 'w') as question_csv:
        question_headers = ['url', 'correct_answer', 'wrong_answer_1', 'wrong_answer_2',
                            'wrong_answer_3', 'slug']
        question_writer = csv.DictWriter(question_csv, fieldnames=question_headers)
        question_writer.writeheader()

        for i in range(num):
            questions = create_quiz(family)
            for question in questions:
                question_writer.writerow(question)


# explore_families("Aster family")
