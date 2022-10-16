"""swe574 URL Configuration

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
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from coLearn.views import (
    learning_space_create_view,
    learning_space_edit_view,
    learning_space_view,
    explore_view,
    sign_up_view,
    sign_in_view,
    profile_view,
    profile_edit_view,
    logout_view,
    question_view,
    question_create_view,
    my_learning_spaces_view,
    search_view
)

urlpatterns = [
    path('', explore_view, name='explore'),
    path('explore/', explore_view, name='explore'),
    path('signup/', sign_up_view, name='sign-up'),
    path('signin/', sign_in_view, name='sign-in'),
    path('logout/', logout_view, name='logout'),
    path('user/<int:user_id>/', profile_view, name='user-profile'),
    path('user/<int:user_id>/edit', profile_edit_view, name='user-profile-edit'),
    path('learningspace/create/', learning_space_create_view, name='learning-space-create'),
    path('learningspace/<int:learning_space_id>/', learning_space_view, name='learning-space'),
    path('learningspace/<int:learning_space_id>/edit/', learning_space_edit_view, name='learning-space-edit'),
    path('learningspace/<int:learning_space_id>/question/<int:question_id>', question_view, name='question'),
    path('learningspace/<int:learning_space_id>/question/create', question_create_view, name='question-create'),
    path('mylearningspaces/', my_learning_spaces_view, name='my-learning-spaces'),
    path('search/', search_view, name='search'),
    path('admin/', admin.site.urls),
]

# If DEBUG is true, the url mapping for the media files
# is appended to the urlpatterns. By doing so, media files
# are accessible during local development. 
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )