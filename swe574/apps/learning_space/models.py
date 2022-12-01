from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

# Model used for Learning Spaces.
from coLearn.models import CoLearnUser
from quiz.models import Quiz


# Answer sent to a Question.
class Answer(models.Model):
    sender = models.ForeignKey(CoLearnUser, on_delete=models.CASCADE, related_name='answer_sender')
    content = models.CharField(max_length=500, blank=True)


# Model used for Questions.
class Question(models.Model):
    question_title = models.CharField(max_length=100)
    author = models.ForeignKey(CoLearnUser, on_delete=models.PROTECT)
    question_content = models.CharField(max_length=500)
    answers = models.ManyToManyField(Answer, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


class LearningSpace(models.Model):
    overview = models.CharField(max_length=1000)
    thumbnail = models.FileField(blank=True)
    prerequisites = ArrayField(models.CharField(max_length=100), blank=True, null=True, default=list)
    title = models.CharField(max_length=100)
    keywords = ArrayField(models.CharField(max_length=100), blank=True, null=True, default=list)
    subscribers = models.ManyToManyField(CoLearnUser, blank=True)
    questions = models.ManyToManyField(Question, blank=True)
    quizzes = models.ManyToManyField(Quiz, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)



