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
        # Obtener la URL de la imagen original antes de guardar
        if self.pk:
            old_instance = Categoria.objects.get(pk=self.pk)
            old_image_url = old_instance.imgenobjeto
        else:
            old_instance = None
            old_image_url = None

        # Guardar el objeto para obtener su ID
        super(Categoria, self).save(*args, **kwargs)

        # Obtener el archivo de imagen
        image_file = self.imgenobjeto

        # Verificar si hay una nueva imagen
        if image_file and (not old_image_url or old_image_url != image_file):
            # Obtener una referencia al bucket de Firebase Storage
            bucket = storage.bucket()

            # Subir el nuevo archivo de imagen a Firebase Storage
            blob = bucket.blob(f'categorias/{self.id}/{image_file.name}')
            with open(image_file.path, 'rb') as file:
                content_type, _ = guess_type(image_file.name)
                blob.upload_from_file(file, content_type=content_type or 'application/octet-stream')

            # Hacer que el blob sea públicamente accesible
            blob.make_public()

            # Obtener la URL pública
            url = blob.public_url

            # Actualizar la URL de la imagen para que apunte a la URL pública
            self.imgenobjeto = url
            super(Categoria, self).save(update_fields=['imgenobjeto'])

            # Eliminar el archivo local si no es necesario
            default_storage.delete(image_file.path)

            # Eliminar la imagen anterior de Firebase Storage
            if old_instance and old_image_url:
                try:
                    old_image_url_str = str(old_image_url)
                    old_blob_name_parts = old_image_url_str.split('/')
                    old_image_name_with_exp = old_blob_name_parts[-1]
                    old_image_name = old_image_name_with_exp.split('?')[0]
                    old_blob = bucket.blob(f'categorias/{self.id}/{old_image_name}')
                    old_blob.delete()
                    print(f"Imagen antigua '{old_blob.name}' eliminada correctamente de Firebase.")
                except Exception as e:
                    print(f"Error al eliminar la imagen antigua de Firebase: {e}")
        else:
            # Si la imagen no ha cambiado, no volver a guardar el objeto
            super(Categoria, self).save(update_fields=['nombre', 'fecha_modificacion'])
    
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
    unityobjeto = models.FileField(verbose_name="ObjProject", max_length=10000, default="")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Objeto")
        verbose_name_plural = ("Objetos")

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # Guardar las URLs de los archivos originales antes de guardar
        if self.pk:
            old_instance = Objeto.objects.get(pk=self.pk)
            old_image_url = old_instance.imgenobjeto
            old_file_url = old_instance.unityobjeto
        else:
            old_instance = None
            old_image_url = None
            old_file_url = None

        # Guardar el objeto para obtener su ID
        super(Objeto, self).save(*args, **kwargs)

        # Subir la nueva imagen si se proporciona
        image_file = self.imgenobjeto
        if image_file and (not old_image_url or old_image_url != image_file):
            self.upload_to_firebase(image_file, 'ObjetoImg', 'imgenobjeto', old_image_url)

        # Subir el nuevo archivo unityobjeto si se proporciona
        unity_file = self.unityobjeto
        if unity_file and (not old_file_url or old_file_url != unity_file):
            self.upload_to_firebase(unity_file, 'AssetsBundle', 'unityobjeto', old_file_url)

    def upload_to_firebase(self, file, folder, field, old_url):
        # Obtener una referencia al bucket de Firebase Storage
        bucket = storage.bucket()

        # Subir el nuevo archivo a Firebase Storage
        blob = bucket.blob(f'{folder}/{self.id}/{file.name}')
        with open(file.path, 'rb') as file_obj:
            content_type, _ = guess_type(file.name)
            blob.upload_from_file(file_obj, content_type=content_type or 'application/octet-stream')

        # Hacer que el blob sea públicamente accesible
        blob.make_public()

        # Obtener la URL pública
        url = blob.public_url

        # Actualizar el campo correspondiente con la nueva URL
        setattr(self, field, url)
        super(Objeto, self).save(update_fields=[field])

        # Eliminar el archivo local si no es necesario
        default_storage.delete(file.path)

        # Eliminar el archivo antiguo de Firebase Storage
        if old_url:
            try:
                old_url_str = str(old_url)
                old_blob_name_parts = old_url_str.split('/')
                old_file_name_with_exp = old_blob_name_parts[-1]
                old_file_name = old_file_name_with_exp.split('?')[0]
                old_blob = bucket.blob(f'{folder}/{self.id}/{old_file_name}')
                old_blob.delete()
                print(f"Archivo antiguo '{old_blob.name}' eliminado correctamente de Firebase.")
            except Exception as e:
                print(f"Error al eliminar el archivo antiguo de Firebase: {e}")

@receiver(pre_delete, sender=Objeto)
def eliminar_archivos_de_firebase(sender, instance, **kwargs):
    if instance.imgenobjeto:
        try:
            image_url = str(instance.imgenobjeto)
            image_path_parts = image_url.split('/')
            image_name_with_exp = image_path_parts[-1]
            image_name = image_name_with_exp.split('?')[0]
            bucket = storage.bucket()
            blob = bucket.blob(f'ObjetoImg/{instance.id}/{image_name}')
            blob.delete()
            print(f"Imagen '{blob.name}' eliminada correctamente de Firebase.")
        except Exception as e:
            print(f"Error al eliminar la imagen de Firebase: {e}")

    if instance.unityobjeto:
        try:
            file_url = str(instance.unityobjeto)
            file_path_parts = file_url.split('/')
            file_name_with_exp = file_path_parts[-1]
            file_name = file_name_with_exp.split('?')[0]
            bucket = storage.bucket()
            blob = bucket.blob(f'AssetsBundle/{instance.id}/{file_name}')
            blob.delete()
            print(f"Archivo '{blob.name}' eliminado correctamente de Firebase.")
        except Exception as e:
            print(f"Error al eliminar el archivo de Firebase: {e}")

    
class Proyecto(models.Model):
    diseñador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Diseñador')
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Cliente')
    nombre = models.CharField(max_length=20, blank=True, null=True, default="Nuevo proyecto")
    unityproyect = models.FileField((""), upload_to=None, max_length=100, default="")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    notas_personales = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = ("Proyecto")
        verbose_name_plural = ("Proyectos")

    def __str__(self):
        return self.nombre