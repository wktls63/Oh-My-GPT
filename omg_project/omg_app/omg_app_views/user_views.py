from django.shortcuts                       import render, redirect
from django.contrib                         import messages
from django.contrib.auth                    import authenticate, login as auth_login, logout as auth_logout
from django.core.mail                       import send_mail
from django.http                            import JsonResponse
from rest_framework_simplejwt.tokens        import RefreshToken, TokenError
from omg_app.models                         import User
from ..forms                                import SignUpForm, LoginForm
from datetime                               import datetime, timedelta

from rest_framework_simplejwt.serializers   import TokenObtainPairSerializer
from rest_framework.views                   import APIView
from rest_framework.response                import Response
from rest_framework                         import status

from omg_app.models                         import *
from omg_app.serializers                    import RegisterSerializer, UserSerializer
from omg_project.settings                   import SECRET_KEY
import jwt

from django.contrib.sites.shortcuts         import get_current_site
from django.template.loader                 import render_to_string
from django.utils.http                      import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail                       import EmailMessage
from django.utils.encoding                  import force_bytes, force_str
from .tokens                                import account_activation_token




''' 기능 관련 '''

def user_login(request):    
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    auth_logout(request)
    messages.success(request, '로그아웃 되었습니다.')
    return redirect('index')
    

def signup(request):
    if request.method == 'POST':
        user = User.objects.create_user(email=request.POST['email'], password=request.POST['password'])
        user.is_active = False
        user.save()
        current_site = get_current_site(request) 
        message = render_to_string('account/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        mail_title = "[OMG] 계정 활성화 확인 이메일"
        mail_to = request.POST["email"]
        email = EmailMessage(mail_title, message, to=[mail_to])
        email.send()
        return redirect("/")

    return render(request, 'login.html')


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExsit):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("/")
    else:
        messages(request, '계정 활성화 오류')
        return render(request, 'index.html')
    return 
    return    

# celery와 같은 백그라언드 작업 큐를 사용하여 주기적인 작업을 스케줄링하도록 설정하면 인증되지 않은 데이터를 자동으로 삭제해줄 수 있음.
# def delete_unverified_users():
#     threshold_time = datetime.now() - timedelta(hours=24)
#     unverified_users = User.objects.filter(is_active=False, date_joined__lte=threshold_time)
#     unverified_users.delete()


''' API 관련 '''

class UserInfoAPIView(APIView):
    """
    유저 조회 API
    """
    def get(self, request, **kwards):
        queryset   = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            res = Response(
                {
                    "user": serializer.data,
                    "message": "register success",

                },
                status = status.HTTP_200_OK,
            )

            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


''' [임시주석처리(회원가입시 토큰 생성 안되게 기능 수정 진행 중) | 김민호]
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                    # 추후 리프레시 토큰 빼도 되는지 보기
                    # access를 
                },
                status = status.HTTP_200_OK,
            )
            
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
    

class AuthView(APIView):

    def post(self, request):
        user = authenticate(
           username = request.data.get("email"), password = request.data.get("password")
        )
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status = status.HTTP_200_OK,
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)