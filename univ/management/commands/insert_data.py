import time

import requests
import random
from django.core.management.base import BaseCommand

from univ import indexings
from univ.models import University, Answer


class Command(BaseCommand):
    help = 'Populate database with question data'

    def handle(self, *args, **kwargs):
        for _ in range(5000):
            random_id = random.randint(400000, 900000)
            user_agent_header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                                               'AppleWebKit/537.36 (KHTML, like Gecko) '
                                               'Chrome/91.0.4472.114 Safari/537.36'}
            response = requests.get(f'https://api.univ100.kr/find/qna/question?questionId={random_id}', headers=user_agent_header)

            if response.status_code == 200:
                data = response.json()

                if data['status'] == 'success':
                    result = data['result']
                    question_data = result['question']
                    answer_data = result.get('answers', [])

                    # Check if the university exists or create a new one

                    # if university doesn't exist and university count is 30, continue
                    if not University.objects.filter(name=question_data['campusName']).exists() and University.objects.count() == 30:
                        continue

                    print(University.objects.count())

                    university, created = University.objects.get_or_create(
                        name=question_data['campusName'],
                        icon=f"https://cf-ui.univ100.kr/campus/{question_data['campusImage']}_160px.png",
                    )

                    if university.id != 78:
                        print('pass')
                        continue

                    try:
                        question = indexings.index_document(university, question_data['title'], question_data['text'])
                    except:
                        continue

                    time.sleep(0.5)

                    # Add answer data related to the question
                    for answer in answer_data:
                        Answer.objects.create(
                            question=question,
                            content=answer['text'],
                        )

                    self.stdout.write(self.style.SUCCESS(
                        f'Processed question "{question_data["title"]}" for university "{university.name}"'))
