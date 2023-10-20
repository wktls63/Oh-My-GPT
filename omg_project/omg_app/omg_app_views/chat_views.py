from django.shortcuts import render
from django.http import JsonResponse
from ..models import Message, ChatRoom, User

def chat(request):
    """
    Args:
        request (_type_): 사용자로부터 받은 request 객체

    Returns:
        type: 페이지
        chat_list: 사용자에 참여한 채팅방 목록
    """
    
    # TODO: user_id 동적으로 변경 (jwt 토큰으로 가쟈오는 것으로)
    user_id = 2    
    user = User.objects.get(id=user_id)
    chat_list = ChatRoom.objects.filter(user_id=user).select_related('model_id')
    chat_list = list(chat_list)
    chat_list.sort(key=lambda x: -x.id)
    
    context = {
        'chat_list': chat_list
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