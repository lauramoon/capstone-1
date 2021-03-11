import requests
import random
import csv
import sys
sys.path.append('../')
import config

TOKEN = config.TREFLE_TOKEN
BASE_URL = f'https://trefle.io/api/v1/plants'


def create_quiz(family):
    """Create lists of plants with fields needed 
    to create quiz of given family. If any API calls fail,
    returns False"""

    plant_list = []
    answers = []

    family_url = get_url(family)

    page_range = get_range(family)

    if page_range < 11:
        return False

    for page in random.sample(range(1, page_range - 1), 10):
        (more_answers, plant) = get_data(page, family_url)

        if plant:
            plant_list.append(plant)
            answers = answers + more_answers
        else: 
            return False

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
    """get data from single trefle.io page of data"""

    plant_url = f'{family_url}&page={page}'

    try:
        raw_plant_list = requests.get(plant_url).json()

        clean_plant_list = clean(raw_plant_list["data"])

        common_names = [plant["common_name"] for plant in clean_plant_list]
        random_plant = random.choice(clean_plant_list)
        common_names.remove(random_plant["common_name"])

        return (common_names, random_plant)

    except:
        return (False, False)


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
    """Get base url for list of plants from given family"""

    url = f'{BASE_URL}?token={TOKEN}'
    url += '&filter_not[common_name]=null&filter_not[image_url]=null'
    if family != 'general':
        url += f'&filter[family_common_name]={family}'
    return url


def get_range(family):
    """get max page number for search results for given family.
    If error in api call, return 0"""

    try:
        first_page = requests.get(get_url(family)).json()
        last_page_num = first_page["links"]["last"].split('page=')[1]
        return int(last_page_num)
    except:
        return 0


def get_plant_info(slug):
    """Get info for specific plant"""

    plant_url = f'{BASE_URL}/{slug}?token={TOKEN}'

    try:
        return requests.get(plant_url).json()["data"]
    except:
        return False


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
    """Export to csv data for 'num' quizzes from given family 
    to use to seed database or to add in bulk later.
    If there is an error in the creation, 
    the file will be empty except for headers"""

    with open(f'{file_name}.csv', 'w') as question_csv:
        question_headers = ['url', 
                            'correct_answer', 
                            'wrong_answer_1', 
                            'wrong_answer_2',
                            'wrong_answer_3', 
                            'slug']
        question_writer = csv.DictWriter(question_csv, fieldnames=question_headers)
        question_writer.writeheader()

        for i in range(num):
            questions = create_quiz(family)
            if questions:
                for question in questions:
                    question_writer.writerow(question)


# create_seed_quizzes('pea_3', 'Pea family', 3)
# explore_families("Flax family")
# print(f'{BASE_URL}/equisetum-hyemale?token={TOKEN}')
