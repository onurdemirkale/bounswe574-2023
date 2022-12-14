from django.db import models

# Create your models here.

# Note: ForeignKey is used to define many-to-one relationships.

# Chat Model that represents a conversation between two users.
from coLearn.models import CoLearnUser


class Chat(models.Model):
    first_user = models.ForeignKey(CoLearnUser, on_delete=models.CASCADE, related_name='chat_initiator')
    second_user = models.ForeignKey(CoLearnUser, on_delete=models.CASCADE, related_name='chat_participant')
    # katilimci = models.ManyToManyField(CoLearnUser, blank=True)
    # first_user_info = models.CharField(max_length=128, unique=True,blank=True)
    # second_user_info = models.CharField(max_length=128, unique=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    

# ChatMessage Model that represents a message that is sent by any
# party during a chat.
class ChatMessage(models.Model):
    sender = models.ForeignKey(CoLearnUser, on_delete=models.PROTECT, related_name='message_sender')
    receiver = models.ForeignKey(CoLearnUser, on_delete=models.PROTECT, related_name='message_receiver')
    text = models.CharField(max_length=200)  # Limited to 200 characters for now.
    file_attachment = models.FileField(blank=True)  # For possible file/image attachments.
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()