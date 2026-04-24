from django import forms
# # Permisos para el login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

# # Para editar el perfil
from .models import User
from django.contrib.auth.forms import UserChangeForm


class PerfilForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'celular', 'telefono_hogar']

# # Form para el login
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'autofocus': True}))
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' not in username:
            raise ValidationError('Ingrese un correo electrónico válido.')
        return username

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Por favor, introduzca un correo electrónico y una contraseña correctos.')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('Esta cuenta está inactiva.')
        return self.cleaned_data
