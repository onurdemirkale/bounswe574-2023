from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
# Learning Space views.
from learning_space.form import LearningSpaceCreateForm, LearningSpaceEditForm, AnswerForm, QuestionForm
from coLearn.models import CoLearnUser
from learning_space.models import LearningSpace, Question, Answer


def learning_space_view(request, learning_space_id):
    learningSpace = LearningSpace.objects.get(pk=learning_space_id)

    # Obtain quizzes and questions.
    quizzes = learningSpace.quizzes.all()
    questions = learningSpace.questions.all()

    # Obtain the subscribers using the LearningSpace model.
    subscribers = learningSpace.subscribers.all()

    user_subscribed = False

    for s in subscribers:
        if s.user.id == request.user.id:
            user_subscribed = True

    user_authenticated = False

    user_id = None

    # If there is a POST request, subscribe/unsubscribe the user.
    if request.POST:
        coLearnUser = CoLearnUser.objects.get(pk=request.user.id)
        if user_subscribed:
            learningSpace.subscribers.remove(coLearnUser)
            learningSpace.save()
        else:
            learningSpace.subscribers.add(coLearnUser)
            learningSpace.save()

        return redirect('/learningspace/%d' % learning_space_id)

    if request.user.is_authenticated:
        user_authenticated = True
        user_id = request.user.id

    relatedSpaces = LearningSpace.objects.filter(keywords__overlap=learningSpace.keywords)

    activity_quizzes = []

    for activity_quiz in quizzes.order_by('-date_created')[:5]:
        quiz_author = activity_quiz.author.user
        quiz_date = activity_quiz.date_created.date()
        temp_tuple = (quiz_author, quiz_date)
        activity_quizzes.append(temp_tuple)

    activity_questions = []

    for activity_question in questions.order_by('-date_created')[:5]:
        question_author = activity_question.author.user
        question_date = activity_question.date_created.date()
        temp_tuple = (question_author, question_date)
        activity_questions.append(temp_tuple)

    context = {
        'title': learningSpace.title,
        'overview': learningSpace.overview,
        'prerequisites': learningSpace.prerequisites,
        'id': learningSpace.id,
        'quizzes': quizzes,
        'questions': questions,
        'subscribers': subscribers,
        'related_spaces': relatedSpaces,
        'user_authenticated': user_authenticated,
        'user_id': user_id,
        'user_subscribed': user_subscribed,
        'activity_quizzes': activity_quizzes,
        'activity_questions': activity_questions
    }

    return render(request, 'learningSpace/learning_space.html', context)


@login_required
def learning_space_create_view(request):
    if request.method == "POST":
        form = LearningSpaceCreateForm(request.POST, request.FILES or None)
        if form.is_valid():
            space_created = LearningSpace.objects.create(**form.cleaned_data)
            if (space_created):
                return redirect('/learningspace/%d' % space_created.id)
    else:
        user_id = None

        if request.user.is_authenticated:
            user_authenticated = True
            user_id = request.user.id

        context = {'user_authenticated': user_authenticated, 'user_id': user_id}
        return render(request, 'learningSpace/learning_space_create.html', context)


@login_required
def learning_space_edit_view(request, learning_space_id):
    learningSpace = LearningSpace.objects.get(pk=learning_space_id)
    if request.method == "POST":
        form = LearningSpaceEditForm(request.POST, request.FILES or None)
        if form.is_valid():
            result = LearningSpace.objects.filter(pk=learning_space_id).update(**form.cleaned_data)
            if (result):
                return redirect('/learningspace/%d' % learning_space_id)

    user_authenticated = False
    user_id = None

    if request.user.is_authenticated:
        user_authenticated = True
        user_id = request.user.id

    context = {
        'title': learningSpace.title,
        'overview': learningSpace.overview,
        'prerequisites': learningSpace.prerequisites,
        'keywords': learningSpace.keywords,
        'id': learningSpace.id,
        'user_authenticated': user_authenticated,
        'user_id': user_id
    }

    return render(request, 'learningSpace/learning_space_edit.html', context)


# Questions views.

@login_required
def question_view(request, learning_space_id, question_id):
    question = Question.objects.get(pk=question_id)
    answers = question.answers.all()

    answerForm = AnswerForm(request.POST or None)
    if (answerForm.is_valid()):
        coLearnUser = CoLearnUser.objects.get(pk=request.user.id)
        answer = Answer.objects.create(sender=coLearnUser, content=answerForm.cleaned_data.get('content'))
        question.answers.add(answer)

        return redirect('/learningspace/%d/question/%d' % (learning_space_id, question_id))

    context = {
        'learning_space_id': learning_space_id,
        'question_id': question_id,
        'question': question,
        'answers': answers
    }

    return render(request, 'question/question.html', context)


@login_required
def question_create_view(request, learning_space_id):
    questionForm = QuestionForm(request.POST or None)
    if (questionForm.is_valid()):
        coLearnUser = CoLearnUser.objects.get(pk=request.user.id)
        question = Question.objects.create(author=coLearnUser,
                                           question_title=questionForm.cleaned_data.get('question_title'),
                                           question_content=questionForm.cleaned_data.get('question_content'))
        learningSpace = LearningSpace.objects.get(pk=learning_space_id)
        learningSpace.questions.add(question)
        learningSpace.save()

        return redirect('/learningspace/%d/question/%d' % (learning_space_id, question.id))
    user_authenticated = False

    user_id = None

    if request.user.is_authenticated:
        user_authenticated = True
        user_id = request.user.id

    context = {'learning_space_id': learning_space_id, 'user_authenticated': user_authenticated, 'user_id': user_id}
    return render(request, 'question/question_create.html', context)


# MyLearningSpaces views.

def my_learning_spaces_view(request):
    coLearnUser = CoLearnUser.objects.get(id=request.user.id)
    myLearningSpaces = LearningSpace.objects.filter(subscribers=coLearnUser)

    user_authenticated = False
    user_id = None

    if request.user.is_authenticated:
        user_authenticated = True
        user_id = request.user.id

    context = {
        'my_learning_spaces': myLearningSpaces,
        'user_authenticated': user_authenticated,
        'user_id': user_id
    }

    return render(request, 'myLearningSpaces/myLearningSpaces.html', context)
