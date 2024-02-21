from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
import chat.routing
from django.core.asgi import get_asgi_application
from django.conf import settings
# from chat import  routing
application=ProtocolTypeRouter(

    {
    "http": get_asgi_application(),
    "websocket":AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})