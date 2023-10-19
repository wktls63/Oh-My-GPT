from django.http import JsonResponse
from ..models import Message

def messages(request, chat_id) :
    """
    Args:
        request (_type_): 사용자로부터 받은 request 객체
        chat_id (_type_): 채팅방 id

    Returns:
        type_: json
        messages: 채팅빙에 해당하는 메세지
    """
    messages = Message.objects.filter(chat_id=chat_id).order_by('send_date').values()
    return JsonResponse(list(messages), safe=False)