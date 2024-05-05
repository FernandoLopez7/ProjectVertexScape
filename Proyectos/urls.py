from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_proyectos, name='index'),
    # Agrega más URLs según sea necesario
]
