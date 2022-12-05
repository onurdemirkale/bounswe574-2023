from django.shortcuts import redirect, render
from quiz.models import Quiz, QuizQuestion
from quiz.forms import quiz_form, question_form
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from learning_space.models import LearningSpace

# Create your views here.
def list_quizes(request, space_id):
    space = LearningSpace.objects.get(id = space_id)
    quizes = Quiz.objects.filter(space = space).order_by('published_date')
    context = {"quizes" : quizes , "space" : space}
    return render(request, template_name="quiz/quiz_page.html" , context = context)

def create_quiz(request,space_id):
    space = LearningSpace.objects.get(id = space_id)    
    if request.method == "POST":
        form_quiz = quiz_form(request.POST)
        if form_quiz.is_valid():
            quiz = form_quiz.save(commit=False)
            quiz.author = request.user
            quiz.space = space
            quiz.save()
            return render(request, 'quiz/quiz_detail.html', {"space" : space , "quiz": quiz})
    else:
        form_quiz = quiz_form()
    return render(request, 'quiz/create_quiz.html', { "space": space , "form_quiz": form_quiz})

def create_question(request,space_id,quiz_id):    
    space = LearningSpace.objects.get(id = space_id)
    quiz = Quiz.objects.get(id = quiz_id)
    form_question = question_form()
    if request.method=='POST':
        form_question = question_form(request.POST)
        if form_question.is_valid():
            question=form_question.save(commit=False)
            question.quiz = quiz
            question.save()
            questions = QuizQuestion.objects.filter(quiz = quiz)
            return render(request, 'quiz/quiz_detail.html', {"space" : space , "quiz" : quiz , "questions":questions})
    return render(request,'quiz/create_question.html',{"space":space,"form_question" : form_question})

def quiz_detail(request,space_id,quiz_id):
    space = LearningSpace.objects.get(id=space_id)
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

        return render(request,'quiz/quiz_result.html',{"space":space, "quiz":quiz, "total_score" : total_score, 'correct_answers':correct_answers})
    else:
        questions= QuizQuestion.objects.filter(quiz = quiz)
        
        return render(request,'quiz/quiz_detail.html',{"space":space, "quiz":quiz, "questions":questions})
    return


