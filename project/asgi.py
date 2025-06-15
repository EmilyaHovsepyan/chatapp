"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from myapp.routing import websocket_urlpatterns  # Import your app's routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from channels.auth import AuthMiddlewareStack  # <-- Add this import!

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(  # <-- This is the fix!
        URLRouter(websocket_urlpatterns)
    ),
})
