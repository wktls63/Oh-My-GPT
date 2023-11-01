import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omg_project.settings")  # 경로 수정

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

def get_application():
    import omg_app.routing as routing

    application = ProtocolTypeRouter(
        {
            "http": django_asgi_app,
            "websocket": AllowedHostsOriginValidator(
                AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
            ),
        }
    )
    return application

application = get_application()