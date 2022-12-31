from django.contrib import admin
from chat.models import Chat,ChatMessage
# Register your models here.


class RoomAdmin(admin.ModelAdmin):
    list_display = ["first_user",'second_user']

    class Meta:
        model=Chat



class MessageAdmin(admin.ModelAdmin):
    list_display = ["user", "room","created_date"]

    class Meta:
        model = ChatMessage
