from django.shortcuts           import render ,get_object_or_404
from rest_framework             import status
from rest_framework.views       import APIView
from rest_framework.response    import Response
from .models                    import SubscriptionProduct, Payment, User
from .serializers               import SubscriptionSerializer ,PaymentSerializer

# 시크릿 키 불러오기
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

        # 사용자 정보 가져오기
        access_token = request.COOKIES.get('access')
        refresh_token = request.COOKIES.get('refresh')    
        payload = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')

        user = User.objects.get(id=payload["user_id"])

        data = {
            "merchant_id" : request.data["merchant_id"],
            "amount" : request.data["amount"],
            "subscription_product_id" : request.data["subscription_product_id"],
            "user_id" : user.id
        }

        serializer = PaymentSerializer(data=data)

        if serializer.is_valid(raise_exception=True):

            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        # serializer                  = PaymentSerializer(data=request.data)

        # if serializer.is_valid(raise_exception=True):

        #     serializer.save()

        #     return Response(serializer.data, status=status.HTTP_200_OK)

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return render(request, 'index.html')

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