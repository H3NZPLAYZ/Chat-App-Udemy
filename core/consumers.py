# chat/consumers.py
import json

from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string
from core.models import Room, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room = self.get_room()
        if not self.room:
            self.close()
            return
        self.user = self.scope["user"]
        print(self.channel_layer)
        print(self.channel_name)
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
        message_obj = Message.objects.create(
            room=self.room,
            user=self.user,
            content=message,
        )

        context = { 'message': message_obj }

        self.send(text_data=render_to_string('partials/message.html', context))
