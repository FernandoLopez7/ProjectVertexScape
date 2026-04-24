from django.contrib import admin
from .models import Categoria, Objeto, Proyecto
# Register your models here.

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_creacion', 'fecha_modificacion']
    search_fields = ['nombre']

admin.site.register(Categoria, CategoriaAdmin)

class ObjetoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'fecha_creacion', 'fecha_modificacion']
    search_fields = ['nombre']
    list_filter = ['categoria']

admin.site.register(Objeto, ObjetoAdmin)

class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'diseñador', 'cliente', 'fecha_creacion', 'fecha_modificacion']
    search_fields = ['nombre']
    list_filter = ['diseñador', 'cliente']
    
admin.site.register(Proyecto, ProyectoAdmin)