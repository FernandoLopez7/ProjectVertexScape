import datetime
from django.db import models

# Create your models here.
# from django.contrib.auth.models import User
# from Usuarios.models import User

# # Variable global para conectar al modelo User
from django.conf import settings
from mimetypes import guess_type

# # Conexion para los archivos e imagenes
from firebase_admin import credentials, storage, initialize_app
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from django.core.files.storage import default_storage


cred = credentials.Certificate(settings.FIREBASE_JSON_PATH)
STORAGE_BUCKET_NAME = 'vertexscape.appspot.com'
initialize_app(cred, {'storageBucket': STORAGE_BUCKET_NAME})


class Categoria(models.Model):
    nombre = models.CharField(max_length=20, blank=True, null=True, default="Categoria")
    imgenobjeto = models.ImageField(verbose_name="Imagen", max_length=1000, default="")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Categoria")
        verbose_name_plural = ("Categorias")

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # Save the object to get its ID
        super(Categoria, self).save(*args, **kwargs)

        # Get the image file
        image_file = self.imgenobjeto

        if image_file:
            # Get a reference to the Firebase Storage bucket
            bucket = storage.bucket()

            # Upload the image file to Firebase Storage
            blob = bucket.blob(f'categorias/{self.id}/{image_file.name}')
            with open(image_file.path, 'rb') as file:
                content_type, _ = guess_type(image_file.name)
                blob.upload_from_file(file, content_type=content_type or 'application/octet-stream')

                    # Get a signed URL with a token that expires in one hour
            expiration = datetime.timedelta(days=3285)
            url = blob.generate_signed_url(expiration=expiration, method='GET')

            # Update the image URL to point to the signed URL
            self.imgenobjeto = url
            super(Categoria, self).save(*args, **kwargs)
            
            default_storage.delete(image_file.name)
    
@receiver(pre_delete, sender=Categoria)
def eliminar_imagen_de_firebase(sender, instance, **kwargs):
    if instance.imgenobjeto:
        try:
            image_url = str(instance.imgenobjeto)
            image_path_parts = image_url.split('/')
            image_name_with_exp = image_path_parts[-1]
            image_name = image_name_with_exp.split('?')[0]
            bucket = storage.bucket()
            blob = bucket.blob(f'categorias/{instance.id}/{image_name}')
            blob.delete()
        except Exception as e:
            # Manejar el error de la manera que prefieras
            print(f"Error al eliminar la imagen de Firebase: {e}")

class Objeto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='Categoria')
    nombre = models.CharField(max_length=20, blank=True, null=True, default="Nuevo Objeto")
    imgenobjeto = models.ImageField(verbose_name="Imagen", max_length=1000, default="")
    # unityobjeto = models.FileField(verbose_name="UnityProject", max_length=10000, default="")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Objeto")
        verbose_name_plural = ("Objetos")

    def __str__(self):
        return self.nombre

    # def save(self, *args, **kwargs):
    #     # Save the object to get its ID
    #     super(Categoria, self).save(*args, **kwargs)

    #     # Get the image file
    #     image_file = self.imgenobjeto

    #     if image_file:
    #         # Get a reference to the Firebase Storage bucket
    #         bucket = storage.bucket()

    #         # Upload the image file to Firebase Storage
    #         blob = bucket.blob(f'objetos/{self.id}/{image_file.name}')
    #         with open(image_file.path, 'rb') as file:
    #             content_type, _ = guess_type(image_file.name)
    #             blob.upload_from_file(file, content_type=content_type or 'application/octet-stream')

    #                 # Get a signed URL with a token that expires in one hour
    #         expiration = datetime.timedelta(days=3285)
    #         url = blob.generate_signed_url(expiration=expiration, method='GET')

    #         # Update the image URL to point to the signed URL
    #         self.imgenobjeto = url
    #         super(Categoria, self).save(*args, **kwargs)
            
    #         default_storage.delete(image_file.name)

# @receiver(pre_delete, sender=Objeto)
# def eliminar_imagen_de_firebase(sender, instance, **kwargs):
#     if instance.imgenobjeto:
#         try:
#             image_url = str(instance.imgenobjeto)
#             image_path_parts = image_url.split('/')
#             image_name_with_exp = image_path_parts[-1]
#             image_name = image_name_with_exp.split('?')[0]
#             bucket = storage.bucket()
#             blob = bucket.blob(f'categorias/{instance.id}/{image_name}')
#             blob.delete()
#         except Exception as e:
#             # Manejar el error de la manera que prefieras
#             print(f"Error al eliminar la imagen de Firebase: {e}")

    
class Proyecto(models.Model):
    diseñador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Diseñador')
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Cliente')
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