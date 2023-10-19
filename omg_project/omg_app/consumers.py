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
    
    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        
        
        chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        message = text_data_json["message"] # 메시지 내용 추출
        sender = text_data_json["sender"]  # 보내는 사람 추출
        # chat = Chat.objects.get(id=chat_id)
        # sender = User.objects.get(id=sender)
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "message": message,
                "send_date": "2023-10-19",
                "sender": sender,  # username을 함께 전송
            }
        )
    
    async def chat_message(self, event):
        message = event["message"]
        send_date = event["send_date"]
        sender = event["sender"]  # username을 추출

        # Send message and username to WebSocket
        await self.send(text_data=json.dumps({
            "type" : "chat_message",
            "message": message,
            "send_date": send_date,
            "sender": sender  # username도 함께 전송
        }))
        
        