from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from .models import CoLearnUser
from learning_space.models import LearningSpace
from .forms import  SignInForm, SignUpForm, UserProfileForm, ProfilePictureForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Explore views.

def explore_view(request):

  learningSpaces = LearningSpace.objects.all()

  user_authenticated = False
  user_id = None
  
  if request.user.is_authenticated:
    user_authenticated = True
    user_id = request.user.id

  context = {
    'learning_spaces' : learningSpaces,
    'user_authenticated': user_authenticated,
    'user_id': user_id
  }

  return render(request, 'explore/explore.html', context)

# Search views.

def search_view(request):

  query = request.GET.get("query")

  learningSpacesQuery = LearningSpace.objects.filter(Q(keywords__icontains=query)| Q(overview__icontains=query) | Q(title__icontains=query))

  user_authenticated = False
  user_id = None
  
  if request.user.is_authenticated:
    user_authenticated = True
    user_id = request.user.id

  context = {
    'learning_spaces' : learningSpacesQuery,
    'user_authenticated': user_authenticated,
    'user_id': user_id
  }

  return render(request, 'search/search.html', context)


# Authentication views.

User = get_user_model()

def sign_up_view(request):
  signUpForm = SignUpForm(request.POST or None)
  if signUpForm.is_valid():
    username = signUpForm.cleaned_data.get('username')
    first_name = signUpForm.cleaned_data.get('first_name')
    last_name = signUpForm.cleaned_data.get('last_name')
    email = signUpForm.cleaned_data.get('email')
    password = signUpForm.cleaned_data.get('password')
    confirm_password = signUpForm.cleaned_data.get('confirm_password') 
    try: 
      user = User.objects.create_user(username, email, password)
      user.first_name = first_name
      user.last_name = last_name
      user.save()
    except:
      user = None
    if user != None:
      login(request, user)
      return redirect('/explore/')
    else:
      request.session['sign_up_failed'] = 1
  return render(request, 'signUp/sign_up.html', {'form':signUpForm})

def sign_in_view(request):
  signInForm = SignInForm(request.POST or None)
  if signInForm.is_valid():
    username = signInForm.cleaned_data.get('username')
    password = signInForm.cleaned_data.get('password')
    user = authenticate(request, username=username, password=password)
    if user != None:
      login(request, user)
      return redirect('/explore/')
    else:
      request.session['authentication_failed'] = 1
  return render(request, 'signIn/sign_in.html', {'form':signInForm})

def logout_view(request):
  logout(request)
  return redirect('/explore/')

# User Profile view.

def profile_view(request, user_id):
  coLearnUser = CoLearnUser.objects.get(pk=user_id)
  learningSpaces = LearningSpace.objects.filter(subscribers=coLearnUser)

  profilePictureForm = ProfilePictureForm(request.POST,request.FILES or None)
  if profilePictureForm.is_valid():
    coLearnUser.profile_picture = profilePictureForm.cleaned_data.get('profile_picture_upload')
    coLearnUser.save()

  user_authenticated = False
  
  if request.user.is_authenticated:
    user_authenticated = True

  profile_owner = False

  if user_id == request.user.id:
    profile_owner = True

  context = {
    'first_name' : coLearnUser.user.first_name,
    'last_name' : coLearnUser.user.last_name,
    'bio' : coLearnUser.bio,
    'background': coLearnUser.background,
    'interests': coLearnUser.interests,
    'user_profile_id': coLearnUser.id,
    'user_id': request.user.id,
    'learning_spaces': learningSpaces,
    'profile_picture': coLearnUser.profile_picture,
    'profile_owner': profile_owner,
    'user_authenticated': user_authenticated
  }

  return render(request, 'profile/profile.html', context)

@login_required
def profile_edit_view(request, user_id):
  coLearnUser = CoLearnUser.objects.get(pk=user_id)
  learningSpaces = LearningSpace.objects.filter(subscribers=coLearnUser)

  userProfileForm = UserProfileForm(request.POST or None)

  if userProfileForm.is_valid():
    coLearnUser.bio = userProfileForm.cleaned_data.get('bio')
    coLearnUser.background = userProfileForm.cleaned_data.get('background')
    coLearnUser.interests = userProfileForm.cleaned_data.get('interests')

    coLearnUser.save()
    
    return redirect('/user/%d' % user_id )

  context = {
    'first_name' : coLearnUser.user.first_name,
    'last_name' : coLearnUser.user.last_name,
    'bio' : coLearnUser.bio,
    'background': coLearnUser.background,
    'interests': coLearnUser.interests,
    'user_id': coLearnUser.id,
    'learning_spaces': learningSpaces,
    'profile_picture': coLearnUser.profile_picture
  }

  return render(request, 'profile/profile_edit.html', context)

# Quizzes views.

@login_required
def quiz_view(request, learning_space_id, quiz_id):

    context = {}

    return render(request, 'quiz/quiz.html', context)

@login_required
def quiz_create_view(request, learning_space_id):

    context = {}

    return render(request, 'quiz/quiz_create.html', context)
