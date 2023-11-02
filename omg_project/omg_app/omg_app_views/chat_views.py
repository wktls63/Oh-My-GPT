from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site

from ..models import Message, ChatRoom, User, AIModel

import jwt
from pathlib import Path
import json
import os

from rest_framework.response import Response
from rest_framework import status

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRETS_DIR = BASE_DIR / '.secrets'
secret = json.load(open(os.path.join(SECRETS_DIR, 'secret.json')))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret['DJANGO_SECRET_KEY']

def chat(request):
    """
    Args:
        request (_type_): 사용자로부터 받은 request 객체

    Returns:
        type: 페이지
        chat_list: 사용자에 참여한 채팅방 목록
    """
     # JWT 토큰에서 사용자 가져오기
    access_token = request.COOKIES.get('access')
    refresh_token = request.COOKIES.get('refresh')    

    payload = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')
    user = User.objects.filter(id=payload['user_id']).first()
    
    # 김나영밖에 모르는 GPT와 민원 GPT 기본 생성
    if user:
        default_model1 = AIModel.objects.get_or_create(model_id="05510328-7794-11ee-b962-0242ac120002", model_name="김나영밖에 모르는 GPT", user_id=user)[0]
        default_model2 = AIModel.objects.get_or_create(model_id="a576640e-794e-11ee-b962-0242ac120002", model_name="민원 GPT", user_id=user)[0]
        default_room1 = ChatRoom.objects.get_or_create(model_id_id=default_model1.model_pk, user_id=user)[0]
        default_room2 = ChatRoom.objects.get_or_create(model_id_id=default_model2.model_pk, user_id=user)[0]
    
    chat_list = ChatRoom.objects.filter(user_id=user).select_related('model_id')
    chat_list = list(chat_list)
    chat_list.sort(key=lambda x: -x.id)
    
    current_site = get_current_site(request)
    
    context = {
        'chat_list': chat_list,
        'user' : user,
        'user_id' : user.id,
        'domain': current_site.domain
    }
    
    return render(request, 'chat.html', context)

def messages(request, chat_id) :
    """
    Args:
        request (_type_): 사용자로부터 받은 request 객체
        chat_id (_type_): 채팅방 id

    Returns:
        type: json
        messages: 채팅방에 해당하는 메세지
    """
    messages = Message.objects.filter(chat_id=chat_id).order_by('send_date').values()
    messages = list(messages)
    messages.sort(key=lambda x: x['send_date'])
    return JsonResponse(list(messages), safe=False)

def delete_messages(request, chat_id):
    if request.method == 'DELETE':
        print(f"delete_messages 진입 : {chat_id}")
        chat = ChatRoom.objects.get(id=chat_id)
        print(chat)
        messages = Message.objects.filter(chat_id=chat_id)
        for message in messages:
            message.delete()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)