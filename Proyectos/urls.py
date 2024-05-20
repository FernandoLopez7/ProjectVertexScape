from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_proyectos, name='index'),
    path('crear/', views.crear_proyecto, name='crear_proyecto'),
    path('actualizar/<int:pk>', views.actualizar_proyecto, name='actualizar_proyecto'),
    path('eliminar/<int:pk>', views.eliminar_proyecto, name='eliminar_proyecto'),
    # Agrega más URLs según sea necesario
]
