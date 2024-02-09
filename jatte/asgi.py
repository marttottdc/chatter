import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jatte.settings')


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

django_asgi_application = get_asgi_application()
from chat import routing


application = ProtocolTypeRouter(
    {
        'http': django_asgi_application ,
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
       )
    }
)
