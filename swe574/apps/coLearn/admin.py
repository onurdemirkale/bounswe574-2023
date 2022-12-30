from django.contrib import admin

from coLearn.models import CoLearnUser
from learning_space.models import LearningSpace
from quiz.models import Quiz
from quiz.models import QuizQuestion
from learning_space.models import Question
from learning_space.models import Answer
from chat.models import Chat
from chat.models import ChatMessage

admin.site.register(CoLearnUser)
admin.site.register(LearningSpace)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Chat)
admin.site.register(ChatMessage)






