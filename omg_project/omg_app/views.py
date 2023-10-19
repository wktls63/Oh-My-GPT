from django.shortcuts           import render
from rest_framework             import status
from rest_framework.views       import APIView
from rest_framework.response    import Response
from .models                    import SubscriptionProduct
from .serializers               import SubscriptionSerializer


# API View
class SubScriptionAPIViewp(APIView):
    """
    구독 서비스 상품 목록 API
    """

    def get(self, request, **kwards):

        queryset   = SubscriptionProduct.objects.all()
        serializer = SubscriptionSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


def index(request):
    return render(request, 'index.html')

def chat(request):
    return render(request, 'chat.html')

def write(request):
    return render(request, 'write.html')

def loading(request):
    return render(request, 'loading.html')

def intro(request):
    return render(request, 'intro.html')

def login(request):
    return render(request, 'login.html')

def center_write(request):
    return render(request, 'center-write.html')

def center(request):
    return render(request, 'center.html')

def payment(request):
    return render(request, 'payment.html')