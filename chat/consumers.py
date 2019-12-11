from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from chat.models import MessageContent
from datetime import datetime

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]
        print('message===', message)
        ret = MessageContent.objects.create(**{"user": user, "message": message})
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))


class AsyncChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # 建立分组
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 离开分组
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        """
        接受消息
        :param text_data:
        :param bytes_data:
        :return:
        """
        user = self.scope["user"]
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # ret = MessageContent.objects.create(**{"user": user, "message": message})
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': "chat_message",
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
            'time': datetime.now().strftime(format("%Y-%m-%d %H:%M:%S"))
        }))