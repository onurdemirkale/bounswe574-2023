from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
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

    # TODO: Obtain annotation server URL from configuration.
    annotation_server_url = "http://google.com"
    }

    # TODO: Replace the request method with a POST request and include
    # annotation content in the data.
    response = requests.get(annotation_server_url, data={})

    if response.status_code > 399:
        return HttpResponseBadRequest("Annotation server returned an bad response.")

    # Redirect the user to the original URL
    return redirect(request.META.get('HTTP_REFERER'))
