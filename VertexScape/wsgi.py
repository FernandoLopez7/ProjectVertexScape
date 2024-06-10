"""
WSGI config for VertexScape project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VertexScape.settings')

application = get_wsgi_application()

if not settings.DEBUG:
    from whitenoise import WhiteNoise
    application = WhiteNoise(application, root=settings.STATIC_ROOT)