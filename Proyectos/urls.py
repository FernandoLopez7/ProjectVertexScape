from django.urls import path
from . import views

urlpatterns = [
    path('imagen/', views.ver_imagen, name='imagen'),
    # Agrega más URLs según sea necesario
]
