from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken, RefreshToken
from django.http import JsonResponse
from jwt.exceptions import ExpiredSignatureError

from rest_framework_simplejwt.tokens import SlidingToken, TokenError


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 쿠키에서 액세스 토큰과 리프레시 토큰을 가져옵니다.
        access_token = request.COOKIES.get('access')
        refresh_token = request.COOKIES.get('refresh')
        print(f"토큰:  {access_token}")
        
        if access_token:
            try:
                # 액세스 토큰 검증
                UntypedToken(access_token)
                SlidingToken(access_token)
            except (InvalidToken, TokenError, ExpiredSignatureError):
                # 액세스 토큰이 유효하지 않을 경우 리프레시 토큰으로 새로운 액세스 토큰 발급
                if refresh_token:
                    try:
                        # 리프레시 토큰 검증 및 새로운 액세스 토큰 발급
                        refresh = RefreshToken(refresh_token)
                        new_access_token = str(refresh.access_token)

                        # 새로운 액세스 토큰을 쿠키에 저장
                        response = self.get_response(request)
                        response.set_cookie('access', new_access_token, httponly=True)
                        return response
                    except (InvalidToken, TokenError, ExpiredSignatureError):
                        # 리프레시 토큰도 유효하지 않을 경우 에러 처리
                        return JsonResponse({"error": "Invalid or expired tokens."}, status=401)
                else:
                    return JsonResponse({"error": "Invalid or expired token."}, status=401)

        return self.get_response(request)