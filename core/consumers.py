# chat/consumers.py
import json

from channels.generic.websocket import WebsocketConsumer
from django.core.mail import message

from core.models import Room, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room = self.get_room()
        if not self.room:
            self.close()
            return
        self.user = self.scope["user"]
        self.accept()

    def get_room(self):
        self.room_slug = self.scope["url_route"]["kwargs"]["room_slug"]
        try:
            return Room.objects.get(slug=self.room_slug)
        except Room.DoesNotExist:
            return None

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        Message.objects.create(
            room=self.room,
            user=self.user,
            content=message,
        )
        message = text_data_json["message"]



        self.send(text_data=json.dumps({"message": message}))