from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api

router = DefaultRouter()
router.register(r'proyectos', api.ProyectoViewSet, basename='proyecto')
router.register(r'categorias-objetos', api.CategoriaObjetosViewSet, basename='categorias-objetos')

urlpatterns = [
    path('', views.listar_proyectos, name='index'),
    path('crear/', views.crear_proyecto, name='crear_proyecto'),
    path('actualizar/<int:pk>', views.actualizar_proyecto, name='actualizar_proyecto'),
    path('eliminar/<int:pk>', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('api/', include(router.urls)),
    path('api/unity-proyecto/', api.UnityProyectoAPIView.as_view(), name='unity-proyecto'),
    path('sceneTest/', views.viewScene, name='websocket'),
    # Agrega más URLs según sea necesario
]

