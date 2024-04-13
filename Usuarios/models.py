# Predeterminado
from django.db import models

# User para FK
from django.contrib.auth.models import User

# Post guardado, genera un nuevo perfil por cada nuevo usuario 
from django.db.models.signals import post_save
from django.dispatch import receiver

# Errores
from django.db import IntegrityError

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=10, verbose_name='Cédula', unique=True, null=True, blank=True, default="17")
    telefono_hogar = models.CharField(max_length=20, verbose_name='Teléfono', null=True, blank=True, default="02")
    celular = models.CharField(max_length=20, verbose_name='Teléfono celular', null=True, blank=True, default="00")
    
    class Meta:
        verbose_name = ("Perfil")
        verbose_name_plural = ("Perfiles")
    
    def __str__(self):
        return self.usuario.username



@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'perfil'):
        try:
            Perfil.objects.create(usuario=instance)
        except IntegrityError:
            pass

@receiver(post_save, sender=User)
def guardar_perfil(sender, instance, **kwargs):
    if hasattr(instance, 'perfil') and instance.perfil.cedula is not None:
        try:
            instance.perfil.save()
        except Exception as e:
            pass