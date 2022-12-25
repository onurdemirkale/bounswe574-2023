from django.shortcuts import render


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

    user_authenticated = False
    user_id = None

    if request.user.is_authenticated:
        user_authenticated = True
        user_id = request.user.id

    context = {
        'user_authenticated': user_authenticated,
        'user_id': user_id
    }

    print('creating an annotation...')

    return render(request, 'annotation/annotations.html', context)
