from django.contrib import admin

# Register your models here.
from .models import Perfil

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

# Registrar la clase UserAdmin personalizada
admin.site.unregister(User)
admin.site.register(User, UserAdmin)



class PerfilAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'telefono_hogar', 'celular']
    # Otros campos que desees mostrar en la lista de perfiles

admin.site.register(Perfil, PerfilAdmin)