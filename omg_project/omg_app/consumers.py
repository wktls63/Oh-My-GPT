import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message, User, AIModel
import aiohttp
import asyncio

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
    
    ## TODO: AI 서버에서 모델 메시지 받아오기
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
        
        sender = text_data_json["sender"]
        user = User.objects.filter(id=sender).first()
            
        if user is None:
            return await self.close() # 인증 실패시 연결 종료

        # 유저 메시지 저장            
        user_message_obj = Message.objects.create(chat_id=chat_room, sender_id=User.objects.get(id=sender), content=message)
        
        # 사용자 메시지를 채팅방 그룹에 전송
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "message": message,
                "send_date": str(dt.datetime.now()),
                "sender": from_,  
            }
        )
        
        # 비동기 태스크로 AI 응답을 가져오는 부분을 실행
        asyncio.create_task(self.get_and_send_ai_response(message, sender, chat_room))

    # TODO: 모델id 동적으로 변경하기
    async def get_and_send_ai_response(self, message, sender, chat_room):
        model_id = "05510328-7794-11ee-b962-0242ac120002"
        ai_response = await self.get_ai_response(message, sender, model_id)
        ai_message_obj = Message.objects.create(chat_id=chat_room, is_user=False, content=ai_response)
        
        # AI 응답을 채팅방 그룹에 전송
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "message": ai_response,
                "send_date": str(dt.datetime.now()),
                "sender": "AI",  
            }
        )
        
        chat_room.last_message = ai_response
        chat_room.save()
    
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
        
    async def get_ai_response(self, message, user_id, model_id):
        # 이 부분을 수정합니다.
        data_payload = {
            "userid": user_id,
            "my_model_id": model_id,
            "message": message
        }
        
        print(data_payload)
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post("http://oreumi.site:1217/generate/message", data=data_payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    print(data)
                    return data['message']
                else:
                    error_message = await response.text()
                    print(f"Error from AI server: {error_message}")
                    return "모델에서 응답을 받아오지 못했습니다."