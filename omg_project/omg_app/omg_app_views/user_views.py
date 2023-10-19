from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from omg_app.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from ..forms import SignUpForm, LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            auth_login(request, user)
            return JsonResponse({'message': '로그인 되었습니다.'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    else:
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
    return render(request, 'signup.html', {'form': form})


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