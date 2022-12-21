"""myWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *
from coLearn.views import explore_view


app_name = 'learning_space'

urlpatterns = [
    path('', explore_view, name='explore_view'),
    path('create/', learning_space_create_view, name='learning-space-create'),
    path('<int:learning_space_id>/', learning_space_view, name='learning_space_view'),
    path('<int:learning_space_id>/edit/', learning_space_edit_view, name='learning-space-edit'),
    path('<int:learning_space_id>/question/<int:question_id>', question_view, name='question'),
    path('<int:learning_space_id>/question/create', question_create_view, name='question-create'),
    path('mylearningspaces/', my_learning_spaces_view, name='my_learning_spaces_view'),
    path('<int:learning_space_id>/add_tags/', add_tags_view, name='add_tags_view')

]