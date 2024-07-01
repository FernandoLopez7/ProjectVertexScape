"""
ASGI config for VertexScape project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import Proyectos.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VertexScape.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            Proyectos.routing.websocket_urlpatterns
        )
    ),
})
