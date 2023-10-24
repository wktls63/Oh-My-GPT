import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message, User, AIModel

import jwt
from pathlib import Path
import json
import os
import datetime as dt



BASE_DIR = Path(__file__).resolve().parent.parent

SECRETS_DIR = BASE_DIR / '.secrets'
secret = json.load(open(os.path.join(SECRETS_DIR, 'secret.json')))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret['DJANGO_SECRET_KEY']


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
    
    ## TODO: 모델이 메시지를 보냈을 경우, jwt 토큰이 없는데 이 경우 처리해주기
    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        
        chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        message = text_data_json["message"] # 메시지 내용 추출
        from_ = text_data_json["from"] # 모델인지 사용자인지 판별
        
        # 채팅방에 마지막 메시지 업데이트
        chat_room = ChatRoom.objects.get(id=chat_id)
        chat_room.last_message = message
        chat_room.save()
        
        
        # 유저한테서 온 메시지라면
        if from_ == 'user':        
            # JWT 토큰에서 사용자 가져오기
            # access_token = self.scope.get('cookies', {}).get('access', None)
            # payload = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')
            # user = User.objects.filter(id=payload['user_id']).first()
            sender = text_data_json["sender"]
            user = User.objects.filter(id=sender).first()
            
            print(user)
            if user is None:
                # 인증 실패시 연결 종료
                return await self.close()       
            
            message_obj = Message.objects.create(chat_id=chat_room, sender_id=User.objects.get(id=sender), content=message)
        
        # 모델이 보낸 메시지라면
        else:
            message_obj = Message.objects.create(chat_id=chat_room, is_user=False, content=message)
        
        # 메시지를 채팅방 그룹에 전송
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "message": message,
                "send_date": str(dt.datetime.now()),
                "sender": from_,  
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
            "sender": sender 
        }))