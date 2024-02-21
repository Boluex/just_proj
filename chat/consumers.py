import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from.models import Message, Chat

class ChatRoomConsumer(AsyncWebsocketConsumer):
   

     async def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name='chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

       
     async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

     async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']

        # Fetch the chat object asynchronously
        chat = await sync_to_async(Chat.objects.get)(room_name=self.room_name)
        other_user = await sync_to_async(lambda: chat.user1 if self.scope['user'] == chat.user2 else chat.user2)()

        # Create a message object asynchronously
        message = await sync_to_async(Message.objects.create)(
            sender=self.scope['user'],
            chat=chat,
            content=message_content
        )

        # Send the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'username': self.scope['user'].username,
                 'other_user': other_user.username
            }
        )   

     async def chat_message(self, event):
        message = event['message']
        username = event['username']
        other_user = event['other_user'] 
        await self.send(text_data=json.dumps({
            'username': username,
            'message': message,
            'other_user': other_user
        }))
