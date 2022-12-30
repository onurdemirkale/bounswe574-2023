from django import forms
from django.contrib.auth.models import User
from quiz.models import Quiz, QuizQuestion

class quiz_form(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ("title","description")

class question_form(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ("question","option1","option2","option3","option4","true_answer")