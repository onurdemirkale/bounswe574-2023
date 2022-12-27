from django import forms

from learning_space.models import LearningSpace
from tags.models import Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class AddTagToSpace(forms.ModelForm):
    class Meta:
        model = LearningSpace
        fields = ['tags']
