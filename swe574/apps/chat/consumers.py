import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from chat.models import ChatMessage, Chat
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print("data: ",text_data_json)
        user=self.scope["user"]
        chat = Chat.objects.get(id=text_data_json["roomName"])

        ChatMessage.objects.create(text=message, sender=chat.first_user, receiver=chat.second_user, chat_id=chat, timestamp=timezone.now())
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message,"user":user.username}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        user=event["user"]
        print(event)
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message,"user":user}))
        