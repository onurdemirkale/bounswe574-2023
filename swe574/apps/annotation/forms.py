from django import forms


class AnnotationForm(forms.Form):
    body_value = forms.CharField()
    target_type = forms.CharField()
    target_value = forms.CharField()
    target_xpath = forms.CharField()
