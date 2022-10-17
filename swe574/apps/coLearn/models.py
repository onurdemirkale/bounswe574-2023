import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver


# Username, first name, last name, password and e-mail adress
# is already handled by the django auth model. 
# The Profile Django model is used to store the extra information
# that relates to the built-in Django User model.
class CoLearnUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Used to extend the Auth User.
    interests = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    background = models.TextField(max_length=1000, blank=True)
    profile_picture = models.FileField(blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    birth_date = models.DateField(null=True, blank=True)


# Signal definition so that Profile model will be automatically
# created/updated when User instances are created/updated.
@receiver(post_save, sender=User)
def create_colearn_user(sender, instance, created, **kwargs):
    if created:
        CoLearnUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_colearn_user(sender, instance, **kwargs):
    instance.colearnuser.save()


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


# Quiz Question Model used by Quiz to store a Question and Answers created by a user.
class QuizQuestion(models.Model):
    question = models.CharField(max_length=500)
    answers = ArrayField(models.CharField(max_length=200))
    correct_answer = models.CharField(max_length=500)


# Model used for Quizzes.
class Quiz(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(CoLearnUser, on_delete=models.PROTECT)
    description = models.CharField(max_length=500)
    questions = models.ManyToManyField(QuizQuestion)
    date_created = models.DateTimeField(auto_now_add=True)


# Model used for Learning Spaces.
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
