from django.shortcuts                       import render
from django.contrib.auth                    import authenticate, login as auth_login, logout as auth_logout
from django.core.mail                       import send_mail
from django.http                            import JsonResponse
from rest_framework_simplejwt.tokens        import RefreshToken
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



''' 기능 관련 '''

def user_login(request):    
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    auth_logout(request)
    return JsonResponse({'message': '로그아웃 되었습니다.'})
    

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # 일단 데이터베이스에 저장하지 않고 인스턴스만 생성
            user.is_active = False  # 활성화 상태를 비활성으로 설정
            user.save()  # 이제 데이터베이스에 저장
            # 이메일 인증 로직
            send_verification_email(request, user)
            return JsonResponse({'message': '이메일로 발송된 인증번호를 확인해주세요.'})
    else:
        form = SignUpForm()
    return render(request, 'login.html', {'form': form})


def send_verification_email(request, user):
    # JWT 토큰 생성
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)

    # 인증 URL 생성 (이 부분은 실제 프로젝트의 URL 구조에 따라 조정해야 함)
    verify_url = f"{request.scheme}://{request.get_host()}/email_verify/{token}/"

    # 이메일 전송
    send_mail (
        '이메일 인증',
        f'이메일 인증 링크: {verify_url}',
        'jyys0531@gmail.com',  # 임의로 김민호 계정으로 작성해둠
        [user.email],
        fail_silently=False,
    )


def verify_email(request, token):
    try:
        # 토큰 검증
        decoded_data = RefreshToken(token)
        user = User.objects.get(id=decoded_data['user_id'])

        # 이메일 검증 상태 업데이트
        user.email_verified = True
        user.save()

        return JsonResponse({'message': '이메일 인증에 성공하였습니다.'})
    except Exception as e:
        return JsonResponse({'error': '이메일 인증에 실패하였습니다. 다시 시도해주세요.'}, status=400)
    

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
            
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status = status.HTTP_200_OK,
            )
            
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)