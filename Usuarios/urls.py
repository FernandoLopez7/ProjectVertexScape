from django.urls import path
from . import views
from . import api
urlpatterns = [
    path('api/login/', api.LoginView.as_view(), name='loginAPI'),
    path('login/', views.iniciar_sesion, name='login'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
]
