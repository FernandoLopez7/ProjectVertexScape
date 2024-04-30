from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'cedula', 'telefono_hogar', 'celular'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email', 'cedula', 'telefono_hogar', 'celular')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

# Registrar la clase UserAdmin personalizada
admin.site.register(User, UserAdmin)