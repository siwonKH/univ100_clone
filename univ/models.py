from django.db import models


class University(models.Model):
    name = models.TextField(max_length=100)
    icon = models.TextField(max_length=500)
    rating = models.IntegerField()
    likes = models.IntegerField()

    class Meta:
        db_table = 'university'


class Question(models.Model):
    title = models.TextField(max_length=100)
    content = models.TextField(max_length=5000)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()
    university_id = models.ForeignKey(University, on_delete=models.CASCADE)

    class Meta:
        db_table = 'question'


class Word(models.Model):
    word = models.TextField(max_length=1000, unique=True)
    global_frequency = models.IntegerField()

    class Meta:
        db_table = 'word'


class InvertedIndex(models.Model):
    word_id = models.ForeignKey(Word, on_delete=models.CASCADE)
    document_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    frequency = models.IntegerField()

    class Meta:
        db_table = 'inverted_index'


class Answer(models.Model):
    content = models.TextField()
    likes = models.IntegerField()
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        db_table = 'answer'
