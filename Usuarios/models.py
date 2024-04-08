# Predeterminado
from django.db import models

# User para FK
from django.contrib.auth.models import User

# Post guardado, genera un nuevo perfil por cada nuevo usuario 
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono_hogar = models.CharField(max_length=20, verbose_name='Teléfono', null=True, blank=True)
    celular = models.CharField(max_length=20, verbose_name='Teléfono celular', null=True, blank=True)
    def __str__(self):
        return self.usuario.username
    # imagen = models.ImageField(_(""), upload_to=None, height_field=None, width_field=None, max_length=None)
    

@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'perfil'):
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def guardar_perfil(sender, instance, **kwargs):
    try:
        instance.perfil.save()
    except Perfil.DoesNotExist:
        pass