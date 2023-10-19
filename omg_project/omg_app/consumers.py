import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connect 진입')
        self.room_name = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = "chat_%s" % self.room_name
        
        # 채널 레이어에 채팅방 추가
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, code):
        # 채널 레이어에서 채팅방 제거
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    async def receive(self, text_data=None, bytes_data=None):
        pass