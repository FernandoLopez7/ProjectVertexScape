from rest_framework import serializers
from .models import Proyecto, Categoria, Objeto

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'
        
        
class ObjetoSerializer(serializers.ModelSerializer):
    objeto3d = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()

    class Meta:
        model = Objeto
        fields = ['nombre', 'objeto3d', 'img']

    def get_objeto3d(self, objeto):
        return self.context['request'].build_absolute_uri(objeto.unityobjeto)

    def get_img(self, objeto):
        return self.context['request'].build_absolute_uri(objeto.imgenobjeto)