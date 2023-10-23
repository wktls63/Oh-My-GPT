from django.shortcuts import render
from django.http import JsonResponse

from ..models import Message, ChatRoom, User

import jwt
from pathlib import Path
import json
import os

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
    user = User.objects.get(id=payload['user_id'])
    print(user)
    chat_list = ChatRoom.objects.filter(user_id=user).select_related('model_id')
    chat_list = list(chat_list)
    chat_list.sort(key=lambda x: -x.id)
    print(chat_list)
    
    context = {
        'chat_list': chat_list,
        'user_id' : user.id
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