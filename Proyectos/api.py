from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Proyecto, Categoria, Objeto
from .serializers import ProyectoSerializer, ObjetoSerializer, UnityProyectoSerializer
from rest_framework.views import APIView
from .firebase import bucket

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
            habitacion_file = serializer.validated_data['habitacion']
            objeto_file = serializer.validated_data['objeto']

            # Verificar la existencia del proyecto
            try:
                proyecto = Proyecto.objects.get(id=id)
            except Proyecto.DoesNotExist:
                return Response({'message': 'Proyecto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

            # Eliminar archivos antiguos en Firebase Storage
            try:
                print("eliminado")
                habitacion_blob = bucket.blob(f'UnityProyect/{id}/habitacion.json')
                habitacion_blob.delete()
            except Exception as e:
                print(f"Error al eliminar el archivo habitacion.json de Firebase: {e}")
            
            try:
                print("eliminado")
                objeto_blob = bucket.blob(f'UnityProyect/{id}/objeto.json')
                objeto_blob.delete()
            except Exception as e:
                print(f"Error al eliminar el archivo objeto.json de Firebase: {e}")

            # Subir archivos actualizados a Firebase Storage
            habitacion_blob = bucket.blob(f'UnityProyect/{id}/habitacion.json')
            habitacion_blob.upload_from_string(habitacion_file, content_type='application/json')
            habitacion_blob.make_public()
            habitacion_url = habitacion_blob.public_url

            objeto_blob = bucket.blob(f'UnityProyect/{id}/objeto.json')
            objeto_blob.upload_from_string(objeto_file, content_type='application/json')
            objeto_blob.make_public()
            objeto_url = objeto_blob.public_url

            # Actualizar el campo unityproyect del proyecto
            proyecto.unityproyect = {
                'id': id,
                'habitacion': habitacion_url,
                'objeto': objeto_url
            }
            proyecto.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
