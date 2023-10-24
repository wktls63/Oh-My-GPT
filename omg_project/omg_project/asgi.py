import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from omg_project.channels_middleware import ChannelsJWTAuthMiddleware  # 추가된 부분

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

import omg_app.routing as routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
            # ChannelsJWTAuthMiddleware(  # 이곳에 추가된 부분
            #     AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
            # )
        ),
    }
)