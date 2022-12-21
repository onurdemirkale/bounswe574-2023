import json

import requests
from django.http import JsonResponse


# Create your views here.
from django.shortcuts import render

from learning_space.models import LearningSpace
from tags.forms import TagForm, AddTagToSpace
from tags.models import Tag


def create_tag_view(request):
    return render(request, 'tags/create_tag.html')


def get_tags_from_db(request, search_query):
    search_query = search_query.capitalize()
    data = list(Tag.objects.filter(name=search_query).values())
    return JsonResponse(data=data, safe=False)


def get_wikidata(request, search_query):
    search_query = ' "' + search_query + '" '
    wikidata_query = {
        """ SELECT distinct ?item ?itemLabel ?itemDescription WHERE{  
  ?item rdfs:label """ + search_query + """@en . 
  ?article schema:about ?item .
  ?article schema:inLanguage "en" .
  ?article schema:isPartOf <https://en.wikipedia.org/>. 
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
  }    
"""
    }
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get('https://query.wikidata.org/sparql', params={'format': 'json', 'query': wikidata_query},
                            headers=headers)
    data = response.json()
    wiki_data = []

    for data in data['results'].get("bindings"):
        if data.get('item'):
            url_value = data.get('item').get('value')
        else:
            url_value = ""
        if data.get('itemLabel'):
            label_value = data.get('itemLabel').get('value')
        else:
            label_value = ""
        if data.get('itemDescription'):
            description = data.get('itemDescription').get('value')
        else:
            description = ""
        json_item = {
            'url': url_value,
            'label': label_value,
            'description': description
        }
        wiki_data.append(json_item)

    json.dumps(wiki_data)
    return JsonResponse(data=wiki_data, safe=False)


def create_tag_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        wikidata_item_url = request.POST.get('wikidata_item_url')
        wikidata_item_label = request.POST.get('wikidata_item_label')
        wikidata_item_description = request.POST.get('wikidata_item_description')

        data = {
            'name': name.title(),
            "wikidata_item_url": wikidata_item_url,
            "wikidata_item_label": wikidata_item_label,
            "wikidata_item_description": wikidata_item_description,
        }

        form = TagForm(data=data)
        if form.is_valid():
            instance = form.save()
            return JsonResponse({'message': 'success', 'id': instance.id})
        else:
            return JsonResponse({'message': 'Form Failed'})
    else:
        form = TagForm(request.POST)
        print(form.errors)
        return JsonResponse({
            'message': 'fail',
            "error": "Posting Error"
        })


def add_tag_to_space(request):
    if request.method == "POST":
        tag_id = request.POST.get("id")
        learning_space_id = request.POST.get("learning_space_id")
        data = {
            "tags": [tag_id,],
        }
        learning_space = LearningSpace.objects.get(pk=learning_space_id)
        form = AddTagToSpace(instance=learning_space, data=data)
        if form.is_valid():
            learning_space.tags.add(Tag.objects.get(id=tag_id))
            return JsonResponse({'message': 'success'})
        else:
            print(form.errors)
            return JsonResponse({'message': 'Form Failed'})
    else:
        return JsonResponse({
            'message': 'fail',
            "error": "Posting Error"
        })

