from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from annotation.forms import AnnotationForm
import requests


def my_annotations_view(request):

    user_authenticated = False
    user_id = None

    if request.user.is_authenticated:
        user_authenticated = True
        user_id = request.user.id

    context = {
        'user_authenticated': user_authenticated,
        'user_id': user_id
    }

    return render(request, 'annotation/annotations.html', context)


def create_annotation_view(request):

    if not request.user.is_authenticated:
        return HttpResponseBadRequest

    user_authenticated = True
    user_id = request.user.id

    # Obtain annotation server URI from environment variables
    annotation_server_uri = os.environ['ANNOTATION_SERVER_URI']

    # Obtain the current host to display in annotation
    host = request.get_host()

    # Obtain the URI of the page that the annotation was generated in
    target_uri = request.META.get('HTTP_REFERER')

    annotationForm = AnnotationForm(request.POST or None)

    # Return a bad request response if the annotation form is not valid
    if not annotationForm.is_valid():
        return HttpResponseBadRequest("Invalid annotation form.")

    # Obtain the annotation attributes from the form
    body_value = annotationForm.cleaned_data.get('body_value')
    target_type = annotationForm.cleaned_data.get('target_type')
    target_value = annotationForm.cleaned_data.get('target_value')
    target_xpath = annotationForm.cleaned_data.get('target_xpath')
    text_position_end = annotationForm.cleaned_data.get('text_position_end')
    text_position_start = annotationForm.cleaned_data.get(
        'text_position_start')

    # Define the annotation body
    annotation_body = {
        "type": "TextualBody",
        "value": body_value,
        "format": "text/html",
        "language": "en"
    }

    if response.status_code > 399:
        return HttpResponseBadRequest("Annotation server returned an bad response.")

    # Redirect the user to the original URL
    return redirect(request.META.get('HTTP_REFERER'))
