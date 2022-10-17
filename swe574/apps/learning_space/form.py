from django.contrib.postgres.forms import SimpleArrayField
from django import forms


class LearningSpaceCreateForm(forms.Form):
    title = forms.CharField(max_length=100)
    overview = forms.CharField(max_length=1000, required=False)
    prerequisites = SimpleArrayField(forms.CharField(max_length=100), delimiter=',', required=False)
    keywords = SimpleArrayField(forms.CharField(max_length=100), delimiter=',', required=False)
    thumbnail = forms.FileField()


class LearningSpaceEditForm(forms.Form):
    title = forms.CharField(max_length=100)
    overview = forms.CharField(max_length=1000, required=False)
    prerequisites = SimpleArrayField(forms.CharField(max_length=100), delimiter=',', required=False)
    keywords = SimpleArrayField(forms.CharField(max_length=100), delimiter=',', required=False)


class AnswerForm(forms.Form):
    content = forms.CharField(max_length=500)


class QuestionForm(forms.Form):
    question_title = forms.CharField(max_length=100)
    question_content = forms.CharField(max_length=500)
