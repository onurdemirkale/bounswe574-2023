from django.shortcuts import redirect, render
from quiz.models import Quiz, QuizQuestion
from quiz.forms import quiz_form, question_form
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from learning_space.models import LearningSpace, CoLearnUser

# Create your views here.
@login_required
def create_quiz(request,learning_space_id):
    learningSpace = LearningSpace.objects.get(id =learning_space_id)
    if request.method == "POST":
        form_quiz = quiz_form(request.POST)
        if form_quiz.is_valid():
            quiz = form_quiz.save(commit=False)
            quiz.author = CoLearnUser.objects.get(pk=request.user.id)
            quiz.save()
            learningSpace.save()
            return render(request, 'quiz/quiz.html', {'learning_space_id': learning_space_id,"learningSpace" : learningSpace , "quiz": quiz})
    else:
        form_quiz = quiz_form()
    return render(request, 'quiz/quiz_create.html', { 'learning_space_id': learning_space_id,"learningSpace": learningSpace , "form_quiz": form_quiz})

@login_required
def create_quiz_question(request,learning_space_id,quiz_id):    
    learningSpace = LearningSpace.objects.get(pk=learning_space_id)
    quiz = Quiz.objects.get(id = quiz_id)
    form_question = question_form()
    if request.method=='POST':
        form_question = question_form(request.POST)
        if form_question.is_valid():
            question=form_question.save(commit=False)
            question.quiz = quiz
            question.save()
            learningSpace.save()
            questions = QuizQuestion.objects.filter(quiz = quiz)
            return render(request, 'quiz/quiz.html', {'learning_space_id': learning_space_id,"learningSpace" : learningSpace , "quiz" : quiz , "questions":questions})
    return render(request,'quiz/create_quiz_question.html',{'learning_space_id': learning_space_id,"learningSpace":learningSpace,"form_question" : form_question})

@login_required
def quiz_detail(request,learning_space_id,quiz_id):
    learningSpace = LearningSpace.objects.get(pk=learning_space_id)
    quiz = Quiz.objects.get(id = quiz_id)
    if request.method == 'POST':
        print(request.POST)
        questions= QuizQuestion.objects.filter(quiz = quiz)
        correct_answers=0
        question_number=0
        for q in questions:
            question_number+=1
            print(request.POST.get(q.question))
            print(q.true_answer)
            print()
            if q.true_answer ==  request.POST.get(q.question):
                correct_answers+=1
            
        total_score = round((correct_answers/question_number) *100)

        return render(request,'quiz/quiz_result.html',{'learning_space_id': learning_space_id,"learningSpace":learningSpace, "quiz":quiz, "total_score" : total_score, 'correct_answers':correct_answers})
    else:
        questions= QuizQuestion.objects.filter(quiz = quiz)
        
        return render(request,'quiz/quiz.html',{'learning_space_id': learning_space_id, "learningSpace":learningSpace, "quiz":quiz, "questions":questions})
    return
