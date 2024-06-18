# tanto unity como el cliente(html) se conectan con esta url
# para comunicarse con el consumer.py de Proyectos\SceneConsumer
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/jsonScene/$', consumers.CameraStreamConsumer.as_asgi()),
    # ws://localhost:8000/ws/jsonScene
    # con views.py y urls,py hago que en django se conecte con http://

    # ws://projectvertexscape.onrender.com/ws/jsonScene/
]