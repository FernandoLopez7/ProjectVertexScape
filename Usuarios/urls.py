from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.iniciar_sesion, name='login'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    # Agrega más URLs según sea necesario
]
