from django.db import models
from django.conf import settings
from coLearn.models import CoLearnUser
from django.utils import timezone

# Create your models here.
class Quiz(models.Model):
    author = models.ForeignKey(CoLearnUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    description = models.CharField(max_length=500)    
    published_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.title

true_choices = [("option1" , "option1"),("option2" ,"option2"),("option3" , "option3"),("option4", "option4"),]

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.CharField(max_length=280,null=True)
    option2 = models.CharField(max_length=280,null=True)
    option3 = models.CharField(max_length=280,null=True)
    option4 = models.CharField(max_length=280,null=True)
    true_answer = models.CharField(max_length=280, choices=true_choices, default= option1, null=True, blank=True)

    def __str__(self):
        return self.question