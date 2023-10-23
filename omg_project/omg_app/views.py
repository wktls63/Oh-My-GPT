from django.shortcuts           import render ,get_object_or_404
from rest_framework             import status
from rest_framework.views       import APIView
from rest_framework.response    import Response
from .models                    import SubscriptionProduct, Payment, User
from .serializers               import SubscriptionSerializer ,PaymentSerializer


# API View
class SubScriptionAPIView(APIView):
    """
    구독 서비스 상품 목록 API
    """

    def get(self, request, **kwards):

        queryset   = SubscriptionProduct.objects.all()
        serializer = SubscriptionSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PaymentValidationView(APIView):

    def post(self, request, **kwards):

        serializer                  = PaymentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return render(request, 'index.html')

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