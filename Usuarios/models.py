# # Predeterminado
from django.db import models

# # User para FK
# from django.contrib.auth.models import User

# # # Post guardado, genera un nuevo perfil por cada nuevo usuario 
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# # # Errores
# from django.db import IntegrityError

# # Para le login
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    cedula = models.CharField(max_length=10, verbose_name='Cédula', unique=True, null=True, blank=True, default="17")
    telefono_hogar = models.CharField(max_length=20, verbose_name='Teléfono', null=True, blank=True, default="02")
    celular = models.CharField(max_length=20, verbose_name='Teléfono celular', null=True, blank=True, default="00")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'