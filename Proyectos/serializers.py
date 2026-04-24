from rest_framework import serializers
from .models import Proyecto, Categoria, Objeto

class ProyectoSerializer(serializers.ModelSerializer):
    diseñador_nombre = serializers.SerializerMethodField()
    cliente_nombre = serializers.SerializerMethodField()
    grupo = serializers.SerializerMethodField()

    class Meta:
        model = Proyecto
        fields = '__all__'

    def get_diseñador_nombre(self, obj):
        return f"{obj.diseñador.first_name} {obj.diseñador.last_name}" if obj.diseñador else None

    def get_cliente_nombre(self, obj):
        return f"{obj.cliente.first_name} {obj.cliente.last_name}" if obj.cliente else None
    
    def get_grupo(self, obj):
        usuario = self.context['request'].user
        if usuario.groups.filter(name='Diseñador').exists():
            return "Diseñador"
        elif usuario.groups.filter(name='Cliente').exists():
            return "Cliente"
        return "Sin grupo"
    
class ObjetoSerializer(serializers.ModelSerializer):
    objeto3d = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()

    class Meta:
        model = Objeto
        fields = ['nombre', 'objeto3d', 'img', 'descripcion', 'tipoHabitacion']

    def get_objeto3d(self, objeto):
        return self.context['request'].build_absolute_uri(objeto.unityobjeto)

    def get_img(self, objeto):
        return self.context['request'].build_absolute_uri(objeto.imgenobjeto)
    
class UnityProyectoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    habitacion = serializers.JSONField()
    objeto = serializers.JSONField()
    material_pared = serializers.CharField()
    material_piso = serializers.CharField()