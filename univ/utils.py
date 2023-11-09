from django.db.models import Prefetch

from univ import indexings
from univ.models import University, Answer


def get_random_20_universities():
    return University.objects.all().order_by('-id')[:20]


def search_university(query):
    return University.objects.filter(name__istartswith=query)


def get_university(university_id):
    return University.objects.get(id=university_id)


def get_10_questions_and_first_answer(university_id):
    university = University.objects.get(id=university_id)

    questions = university.question_set.all().order_by('-id')[:10]

    for question in questions:
        question.first_answer = question.answer_set.first()

    return questions


def get_all_questions_and_first_answer(university_id):
    university = University.objects.get(id=university_id)

    questions = university.question_set.all().order_by('-id')[:50]

    for question in questions:
        question.first_answer = question.answer_set.first()

    return questions


# add question
def add_question(university_id, title, content):
    university = University.objects.get(id=university_id)

    question = indexings.index_document(university, title, content)

    # question = university.question_set.create(title=title, content=content)

    return question


def search_questions(university_id, query):
    results = indexings.search(university_id, query)
    return results
