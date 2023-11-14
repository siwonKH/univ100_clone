from django.db import transaction
from django.db.models import F, Sum, Subquery, OuterRef, Prefetch, ExpressionWrapper, FloatField, Value, Q
from django.db.models.functions import Cast
from konlpy.tag import Komoran

from univ.models import InvertedIndex, Question, Word, Answer

kom = Komoran()


def tokenize(text):
    tokens = kom.pos(text)
    tokens = [word[0] for word in tokens]
    return tokens


@transaction.atomic
def index_document(university, title, content):
    # Tokenize the document content
    tokens = tokenize(title + " " + content)

    # Calculate the frequency of each token before removing duplicates
    token_frequencies = {token: tokens.count(token) for token in tokens}

    # Create a new Document instance
    document = university.question_set.create(title=title, content=content)

    for token, frequency in token_frequencies.items():
        # Update the global frequency of each word or create a new one if it doesn't exist
        word, created = Word.objects.get_or_create(word=token)
        if not created:
            word.global_frequency += 1
            word.save(update_fields=['global_frequency'])
        else:
            word.global_frequency = 1  # Set initial frequency to 1 for new words
            word.save()

        # Update the InvertedIndex
        inverted_index, created = InvertedIndex.objects.get_or_create(word=word, question=document, defaults={'frequency': frequency})
        if not created:
            inverted_index.frequency += frequency
            inverted_index.save(update_fields=['frequency'])

    return document


def search(university_id, query):
    print(query)
    tokens = tokenize(query)
    print(tokens)

    document_scores = {}

    for token in tokens:
        results = InvertedIndex.objects.filter(
            word__word=token,
            question__university=university_id
        ).annotate(
            global_frequency=F('word__global_frequency'),
            score=ExpressionWrapper(
                Cast('frequency', FloatField()) / (1 + Cast('global_frequency', FloatField())),
                output_field=FloatField()
            )
        ).select_related('question__answer_set').values('question_id', 'score', 'question__title', 'question__content',
                                                        'question__answer__content')

        for result in results:
            doc_id = result['question_id']
            score = result['score']
            question_title = result['question__title']
            question_content = result['question__content']
            answer_content = result['question__answer__content']

            if doc_id in document_scores:
                document_scores[doc_id]['score'] += score
            else:
                document_scores[doc_id] = {
                    'id': doc_id,
                    'score': score,
                    'title': question_title,
                    'content': question_content,
                    'answer': answer_content,
                }

    questions = sorted(document_scores.items(), key=lambda item: item[1]['score'], reverse=True)

    new_question_list = []
    for question in questions:
        new_question_list.append(question[1])

    return new_question_list


def legacy_search(university_id, query):
    results = Question.objects.filter(
        Q(content__contains=query) | Q(title__contains=query),
        university=university_id
    ).select_related('answer_set').values('id', 'title', 'content', 'answer__content')

    document_scores = {}

    for result in results:
        doc_id = result['id']
        question_title = result['title']
        question_content = result['content']
        answer_content = result['answer__content']

        document_scores[doc_id] = {
            'id': doc_id,
            'title': question_title,
            'content': question_content,
            'answer': answer_content,
        }

    questions = sorted(document_scores.items(), key=lambda item: item[1]['id'], reverse=True)

    new_question_list = []
    for question in questions:
        new_question_list.append(question[1])

    return new_question_list
