from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from rest_framework_simplejwt.tokens import UntypedToken, RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt.exceptions import ExpiredSignatureError

from omg_app.models import User

class ChannelsJWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        # scope에서 쿠키를 가져옵니다.
        # cookies = scope.get('headers', {}).get(b'cookie', b'').decode('utf-8')
        
        cookie_header = None
        for header_name, header_value in scope.get('headers', []):
            if header_name == b'cookie':
                cookie_header = header_value
                break

        if cookie_header:
            cookies = cookie_header.decode('utf-8')
        else:
            cookies = ''
        
        access_token = self._get_cookie_value(cookies, 'access')
        refresh_token = self._get_cookie_value(cookies, 'refresh')

        if access_token:
            try:
                # 액세스 토큰 검증
                UntypedToken(access_token)
                scope['user'] = await self.get_user_from_token(access_token)
            except (InvalidToken, TokenError, ExpiredSignatureError):
                # 액세스 토큰이 만료되었지만 유효한 리프레시 토큰이 있을 경우
                if refresh_token:
                    try:
                        # 리프레시 토큰 검증 및 새로운 액세스 토큰 발급
                        refresh = RefreshToken(refresh_token)
                        new_access_token = str(refresh.access_token)

                        # 여기서는 새로운 액세스 토큰을 쿠키에 설정할 수 없으므로,
                        # 클라이언트에게 액세스 토큰이 만료되었다고 알리고 연결을 종료합니다.
                        await send({
                            'type': 'websocket.close',
                            'code': 4000  # custom close code
                        })
                        return  # 종료
                    except (InvalidToken, TokenError, ExpiredSignatureError):
                        scope['user'] = AnonymousUser()
                else:
                    scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    def _get_cookie_value(self, cookies, key):
        # 쿠키 문자열에서 원하는 키의 값을 가져옵니다.
        for cookie in cookies.split(';'):
            cookie = cookie.strip()
            if cookie.startswith(key + '='):
                return cookie.split('=', 1)[1].strip()
        return None

    @database_sync_to_async
    def get_user_from_token(self, token):
        # 액세스 토큰에서 user 정보를 가져오는 로직
        decoded_data = UntypedToken(token)
        return User.objects.get(id=decoded_data['user_id'])
