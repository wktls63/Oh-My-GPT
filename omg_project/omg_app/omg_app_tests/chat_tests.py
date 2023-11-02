from django.test import TestCase, RequestFactory

# Create your tests here.
from channels.testing import ChannelsLiveServerTestCase
from channels.db import database_sync_to_async
from rest_framework.test import APIClient
from channels.testing import WebsocketCommunicator

from channels.routing import ProtocolTypeRouter, URLRouter

from omg_app.models import *
from omg_app.routing import websocket_urlpatterns
from omg_app.omg_app_views import chat_views

import json

application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns),
})

class ChatTest(ChannelsLiveServerTestCase):
    def setUp(self):
        # 이메일 인증이 활성된 유저 생성
        self.user = User.objects.create(email="testuser@test.com", password="password", is_active=True)
        
        # AI모델 생성
        self.model = AIModel.objects.create(model_id="11111111-1111-1111-1111-111111111111", model_name="test_model", user_id=self.user)
        
        # 채팅방 생성
        self.room = ChatRoom.objects.create(model_id=self.model, user_id=self.user, last_message="This is test model")
        
        # 메시지 생성
        self.message1 = Message.objects.create(chat_id=self.room, sender_id=self.user, content="Hello")
        self.message2 = Message.objects.create(chat_id=self.room, sender_id=self.user, content="World")
        
        self.client = APIClient()
        self.factory = RequestFactory()
        
    @database_sync_to_async
    def create_message(self, user, chat_room, content):
        return Message.objects.create(chat_id=chat_room, sender_id=user, content=content)
    
    async def test_can_connect_to_chat(self):
        communicator = WebsocketCommunicator(application,  path=f"/ws/chat/{self.room.id}/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
    
    async def test_can_send_mesage(self):
        communicator = WebsocketCommunicator(application,  path=f"/ws/chat/{self.room.id}/")
        connected, subprotocol = await communicator.connect()
        
        await communicator.send_json_to({
            "type" : "chat_message",
            "message" : "Hello, World!",
            "sender" : self.user.id,
            "from" : 'user'
        })
        
        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "chat_message")
        self.assertEqual(response["message"], "Hello, World!")
        self.assertEqual(response["sender"], 'user')
    
    def test_can_get_messages(self):
        request = self.factory.get(f"messages/{self.room.id}/")
        request.user = self.user
        response = chat_views.messages(request, chat_id=self.room.id)

        # JsonResponse에서 데이터 가져오기
        messages_data = json.loads(response.content)

        # 반환된 메시지의 수 확인
        self.assertEqual(len(messages_data), 2)

        # 반환된 메시지의 내용 확인
        self.assertEqual(messages_data[0]['content'], "Hello")
        self.assertEqual(messages_data[1]['content'], "World")