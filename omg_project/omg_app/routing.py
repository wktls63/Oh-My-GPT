from django.urls import re_path
from . import consumers
# from channels.routing import ProtocolTypeRouter, URLRouter
# from omg_project.channels_middleware import ChannelsJWTAuthMiddleware

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<chat_id>\d+)/$", consumers.ChatConsumer.as_asgi()),
]

# application = ProtocolTypeRouter({
#     'websocket': ChannelsJWTAuthMiddleware(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })