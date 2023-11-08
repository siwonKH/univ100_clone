from django.db.models import Prefetch

from univ import indexings
from univ.models import University, Answer


def get_random_12_universities():
    return University.objects.all()[:12]


def search_university(query):
    return University.objects.filter(name__istartswith=query)


def get_university(university_id):
    return University.objects.get(id=university_id)


def get_10_questions_and_first_answer(university_id):
    university = University.objects.get(id=university_id)

    # first_answer_qs = Answer.objects.filter(question__university=university)[:1]
    #
    # # Prefetch the first answer for each question using 'Prefetch'
    # questions = university.question_set.prefetch_related(
    #     Prefetch('answer_set', queryset=first_answer_qs, to_attr='first_answer')
    # ).all()[:10]
    # return questions

    # Get the first 10 questions
    questions = university.question_set.all()[:10]

    # Now iterate over the questions and get the first answer for each one
    for question in questions:
        question.first_answer = question.answer_set.first()

    return questions


def get_all_questions_and_first_answer(university_id):
    university = University.objects.get(id=university_id)

    questions = university.question_set.all()

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
