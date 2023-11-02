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
    
class UserSubScriptionAPIView(APIView):
    """
    유저의 구독 서비스 상품을 불러오는 API
    """

    def get(self, request, **kwards):

        access_token = request.COOKIES.get('access')   
        payload = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')
        user = User.objects.get(id=payload["user_id"])

        queryset = Payment.objects.filter(user_id=user.id)
        print(queryset)
        serializer = PaymentSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PaymentValidationView(APIView):
    """
    결제 요청 POST를 받으면 결제를 진행하는 API
    """

    def post(self, request, **kwards):

        # JWT 토큰에서 유저 정보 가져오기
        access_token = request.COOKIES.get('access')   
        payload = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')
        user = User.objects.get(id=payload["user_id"])

        # 유저 정보에서 해당 유저의 결제 내역을 조회
        user_payment_object = Payment.objects.filter(user_id=user.id).first()

        # 결제시 requset 받는 데이터
        data = {
                "merchant_id" : request.data["merchant_id"],
                "amount" : request.data["amount"],
                "subscription_product" : request.data["subscription_product_id"],
                "payment_status" : request.data["status"],
                "user" : user.id
            }
  
        payment_amount = request.data['amount']
        user_subscription_item = request.data["subscription_product_id"]

        # 시리얼 라이저에 request 데이터 전달
        serializer = PaymentSerializer(data=data)

        # 유저가 결제내역이 없다면 결제를 진행
        if user_payment_object is None:

            if serializer.is_valid(raise_exception=True):

                # 유저 구독 상품을 GPT Pro 로 업데이트
                if user_subscription_item == 1:

                    user.payment_status = User.PAYMENT_PRO

                    user.save()

                    serializer.save()

                    return Response(serializer.data, status=status.HTTP_200_OK)

                # 유저 구독 상품을 GPT Pro Plus 로 업데이트
                elif user_subscription_item == 2:

                    user.payment_status = User.PAYMENT_PRO_PLUS

                    user.save()

                    serializer.save()

                    return Response(serializer.data, status=status.HTTP_200_OK)

                # 유저 구독 상품을 GPT Pro Enterprise 로 업데이트
                elif user_subscription_item == 3:

                    user.payment_status = User.PAYMENT_ENTERPRISE

                    user.save()

                    serializer.save()

                    return Response(serializer.data, status=status.HTTP_200_OK)

                else:

                    user.payment_status = User.PAYMENT_BASIC

                    user.save()

                    serializer.save()

                    return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 유저가 똑같은 상품의 결제 내역이 있으면
        elif user_payment_object.amount == payment_amount:

            serializer.is_valid(raise_exception=True)

            return Response(serializer.errors, status=status.HTTP_423_LOCKED)

        # 유저가 다른 상품의 결제 내역이 있으면
        elif user_payment_object.amount != payment_amount:

            serializer.is_valid(raise_exception=True)

            return Response(serializer.errors, status=status.HTTP_418_IM_A_TEAPOT)
        
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