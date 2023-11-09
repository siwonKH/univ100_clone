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
    tokens = tokenize(query)

    print(tokens)

    # Build a queryset that represents the score subquery for a given token
    def score_subquery(token):
        return Subquery(
            InvertedIndex.objects.filter(
                Q(word__word__icontains=token),
                question__university_id=university_id,
                question=OuterRef('pk')
            ).annotate(
                score=F('frequency') / (1 + Cast('word__global_frequency', output_field=FloatField()))
            ).values('score')
        )

    # Define a Prefetch object for the first answer
    first_answer_prefetch = Prefetch(
        'answer_set',
        queryset=Answer.objects.order_by('id'),
        to_attr='first_answer'
    )

    # Start with a queryset for Questions that belong to the given university
    questions = Question.objects.filter(university_id=university_id).prefetch_related(first_answer_prefetch)

    for token in tokens:
        # Annotate each question with the score for the current token
        questions = questions.annotate(**{
            f'score_{token}': score_subquery(token)
        })

    # Sum up all the individual token scores for each question
    score_expressions = [F(f'score_{token}') for token in tokens]
    questions = questions.annotate(
        raw_total_score=Sum(*score_expressions)
    ).filter(
        raw_total_score__isnull=False
    )

    # Multiply the raw total score by 100 using ExpressionWrapper
    questions = questions.annotate(
        total_score=ExpressionWrapper(
            F('raw_total_score') * Value(100),
            output_field=FloatField()
        )
    ).order_by('-total_score')

    # Here we're iterating over each question to attach the first answer
    for question in questions:
        question.first_answer = question.first_answer[0] if question.first_answer else None

        print(question.total_score)

    return questions
