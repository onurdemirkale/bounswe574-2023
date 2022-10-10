from django.contrib import admin

from coLearn.models import CoLearnUser
from coLearn.models import LearningSpace
from coLearn.models import Quiz
from coLearn.models import QuizQuestion
from coLearn.models import Question
from coLearn.models import Answer
from coLearn.models import Chat
from coLearn.models import ChatMessage

admin.site.register(CoLearnUser)
admin.site.register(LearningSpace)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Chat)
admin.site.register(ChatMessage)






