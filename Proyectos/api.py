from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Proyecto, Categoria, Objeto
from .serializers import ProyectoSerializer, ObjetoSerializer, UnityProyectoSerializer
from rest_framework.views import APIView
from .firebase import bucket
import json

class ProyectoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Proyecto.objects.none()
        usuario = self.request.auth.user
        if usuario.groups.filter(name='Diseñador').exists():
            return Proyecto.objects.filter(diseñador=usuario)
        else:
            return Proyecto.objects.filter(cliente=usuario)

class CategoriaObjetosViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all()
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
    
class UnityProyectoAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UnityProyectoSerializer(data=request.data)
        if serializer.is_valid():
            id = serializer.validated_data['id']
            habitacion = json.loads(serializer.validated_data['habitacion'])
            objeto = json.loads(serializer.validated_data['objeto'])
            material_pared = serializer.validated_data['material_pared']
            material_piso = serializer.validated_data['material_piso']
            
            # Verificar la existencia del proyecto
            try:
                proyecto = Proyecto.objects.get(id=id)
            except Proyecto.DoesNotExist:
                return Response({'message': 'Proyecto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

            # Actualizar el campo unityproyect del proyecto
            unityproyect_data = proyecto.unityproyect or {}
            unityproyect_data.update({
                'id': id,
                'habitacion': habitacion,
                'objeto': objeto,
                'material_piso': material_piso,
                'material_pared': material_pared
                
            })

            proyecto.unityproyect = unityproyect_data
            proyecto.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
