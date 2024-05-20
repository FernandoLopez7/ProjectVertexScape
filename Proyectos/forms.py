from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Proyecto

User = get_user_model()


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['cliente', 'nombre', 'notas_personales']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cliente_group = Group.objects.get(name='Cliente')
        if not self.instance.pk:
            self.fields['cliente'].queryset = User.objects.filter(
                groups=cliente_group)
        else:
            # Si el proyecto ya tiene un ID (es decir, está siendo actualizado), desactivar el campo de cliente
            self.fields['cliente'].disabled = True
