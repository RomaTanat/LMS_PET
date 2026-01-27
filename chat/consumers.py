# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Message, Room 
from .ai_bot import get_ai_response # <--- ИСПРАВЛЕННЫЙ ИМПОРТ

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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

    # --- Хелперы для работы с БД (ОК) ---
    @sync_to_async
    def create_message(self, room, user, content, is_ai_response=False):
        return Message.objects.create(
            room=room,
            user=user if not is_ai_response else None,
            content=content,
            is_ai_response=is_ai_response
        )

    @sync_to_async
    def get_room_and_history(self, room_name):
        room, created = Room.objects.get_or_create(name=room_name, defaults={'slug': room_name})
        history = Message.objects.filter(room=room).order_by('-timestamp')[:10]
        formatted_history = []
        for msg in reversed(history):
            role = 'assistant' if msg.user is None or msg.is_ai_response else 'user'
            formatted_history.append({'role': role, 'content': msg.content})
        return room, formatted_history

    # --- ГЛАВНЫЙ МЕТОД RECEIVE С AI-ЛОГИКОЙ (ОК) ---
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_message = text_data_json['message']
        user = self.scope['user']

        if user.is_anonymous:
            return

        room, history = await self.get_room_and_history(self.room_name)
        await self.create_message(room, user, user_message)

        # 3. Отправка сообщения пользователя
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': user_message,
                'username': user.username,
                'is_ai': False
            }
        )

        # 4. Вызов DeepSeek AI ТОЛЬКО для AI-комнат
        if self.room_name.startswith('mentor_') or self.room_name == 'ai_session':
            ai_response_text = await sync_to_async(get_ai_response)(user_message, history)

            # 5. Сохранение ответа AI
            ai_username = "DeepSeek AI"
            await self.create_message(room, None, ai_response_text, is_ai_response=True)

            # 6. Отправка ответа AI
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': ai_response_text,
                    'username': ai_username,
                    'is_ai': True
                }
            )

    # --- МЕТОД CHAT_MESSAGE СТРУКТУРИРОВАННОГО ВЫВОДА (ОК) ---
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event.get('username', 'Anonymous'),
            'is_ai': event.get('is_ai', False)
        }))
