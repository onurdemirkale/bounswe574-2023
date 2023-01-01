from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse, HttpResponseBadRequest
from annotation.forms import AnnotationForm
from datetime import datetime
import json
import requests
import os
from coLearn.models import CoLearnUser


def my_annotations_view(request):
    
    if not request.user.is_authenticated:
        return HttpResponseBadRequest

    user_authenticated = True
    user_id = request.user.id
    
    # Obtain annotation server URI from environment variables
    annotation_server_uri = os.environ['ANNOTATION_SERVER_URI']
    
    # Obtain the current host
    host = request.get_host()
    
    # Obtain all annotations created by the user using requests library
    response = requests.get("{}/annotation/?creator=http://{}/user/{}".format(annotation_server_uri, host, user_id))
    
    response_json = response.json()
    
    annotation_data = response_json.get("data")
    
    # Obtain the user information
    coLearnUser = CoLearnUser.objects.get(pk=user_id)
    
    annotations = []

    for annotation in annotation_data:
        
        temp = {
            "value": ((annotation.get("content")).get("body")).get("value"),
            "date_created": datetime.fromisoformat(((annotation.get("content")).get("created"))),
            "source_uri": ((annotation.get("content")).get("target")).get("source"),
            "selector": ((annotation.get("content")).get("target")).get("selector"),
            "type": ((annotation.get("content")).get("target")).get("type"),
            "username" : coLearnUser.user.username,
        }
        
        annotations.append(temp)

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

    # Define the target only using XPathSelector if the target type is Image
    if target_type == 'Image':

        target = {
            "source": target_uri,
            "type": "Image",
            "selector": {
                "type": "XPathSelector",
                "value": target_xpath,
            }
        }

    # Define the target using XPathSelector and a refinedBy attribute if the
    # target type is text
    if target_type == 'Text':

        target = {
            "source": target_uri,
            "language": "en",
            "type": "Text",
            "selector": {
                "type": "XPathSelector",
                "value": target_xpath,
                "refinedBy": {
                    "type": "TextPositionSelector",
                    "start": text_position_start,
                    "end": text_position_end
                }
            }
        }

    # Define the annotation
    annotation = {
        "@context": "http://www.w3.org/ns/anno.jsonld",
        # The annotation ID (URI) is implemeneted by the annotation server
        "id": None,
        "type": "Annotation",
        "creator": "http://{}/user/{}".format(host, user_id),
        "created": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "modified": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "generated": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "body": annotation_body,
        "target": target
    }

    # Perform a POST request to the annotation server with the generated annotation
    response = requests.post("{}/annotation/create".format(annotation_server_uri), json={"data":annotation})

    # Return a bad request response if the annotation server returned a bad response
    if response.status_code > 399:
        return HttpResponseBadRequest("Annotation server returned an bad response.")

    # Redirect the user to the original URL
    return redirect(request.META.get('HTTP_REFERER'))
