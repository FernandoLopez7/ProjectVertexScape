from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Proyecto, Categoria, Objeto
from .serializers import ProyectoSerializer, ObjetoSerializer

class ProyectoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.auth.user
        if usuario.groups.filter(name='Diseñador').exists():
            return Proyecto.objects.filter(diseñador=usuario)
        else:
            return Proyecto.objects.filter(cliente=usuario)

class CategoriaObjetosViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ObjetoSerializer

    def list(self, request):
        categorias = Categoria.objects.all()
        data = []

        for categoria in categorias:
            objetos = Objeto.objects.filter(categoria=categoria)
            objetos_data = self.get_serializer(objetos, many=True).data

            categoria_data = {
                'categoria': categoria.nombre,
                'url': request.build_absolute_uri(categoria.imgenobjeto),
                'Objetos': objetos_data
            }

            data.append(categoria_data)

        return Response(data)