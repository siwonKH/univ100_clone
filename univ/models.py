from django.contrib.auth.models import User
from django.db import models


class University(models.Model):
    name = models.TextField(max_length=100)
    icon = models.TextField(max_length=500)
    rating = models.IntegerField(default=90)
    likes = models.IntegerField(default=0)

    class Meta:
        db_table = 'university'


class Question(models.Model):
    title = models.TextField(max_length=100)
    content = models.TextField(max_length=5000)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    class Meta:
        db_table = 'question'

        indexes = [
            models.Index(fields=['title'], name='idx_title'),
            models.Index(fields=['content'], name='idx_content'),
        ]


class Word(models.Model):
    word = models.TextField(max_length=1000, unique=True)
    global_frequency = models.IntegerField(default=0)

    class Meta:
        db_table = 'word'
        indexes = [
            models.Index(fields=['word'], name='idx_word'),
        ]


class InvertedIndex(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    frequency = models.IntegerField(default=0)

    class Meta:
        db_table = 'inverted_index'
        indexes = [
            models.Index(fields=['word'], name='idx_word_id'),
            models.Index(fields=['question'], name='idx_question_id'),
        ]


class Answer(models.Model):
    content = models.TextField()
    likes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        db_table = 'answer'


class UserLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_like'
