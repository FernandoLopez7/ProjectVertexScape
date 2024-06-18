from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

# Deshabilitar CSRF para las vistas del panel de administración
admin.site.login = csrf_exempt(admin.site.login)
admin.site.logout = csrf_exempt(admin.site.logout)
admin.site.index = csrf_exempt(admin.site.index)
admin.site.password_change = csrf_exempt(admin.site.password_change)