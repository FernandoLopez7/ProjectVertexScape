from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Proyecto(models.Model):
    diseñador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Diseñador')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Cliente')
    nombre = models.CharField(max_length=20, blank=True, null=True, default="Nuevo proyecto")
    # unityproyect = models.FileField((""), upload_to=None, max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    notas_personales = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = ("Proyecto")
        verbose_name_plural = ("Proyectos")

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=20, blank=True, null=True, default="Categoria")
    # imgenobjeto = models.ImageField((""), upload_to=None, height_field=None, width_field=None, max_length=None)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Categoria")
        verbose_name_plural = ("Categorias")

    def __str__(self):
        return self.nombre


class Objeto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='Categoria')
    nombre = models.CharField(max_length=20, blank=True, null=True, default="Nuevo Objeto")
    # imgenobjeto = models.ImageField((""), upload_to=None, height_field=None, width_field=None, max_length=None)
    # unityobjeto = models.FileField((""), upload_to=None, max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Objeto")
        verbose_name_plural = ("Objetos")

    def __str__(self):
        return self.nombre