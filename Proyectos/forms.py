from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Proyecto
import json

User = get_user_model()


class ProyectoForm(forms.ModelForm):
    habitacion = forms.CharField(widget=forms.Textarea, required=False)
    objeto = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = Proyecto
        fields = ['cliente', 'nombre', 'notas_personales', 'habitacion', 'objeto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cliente_group = Group.objects.get(name='Cliente')
        if not self.instance.pk:
            self.fields['cliente'].queryset = User.objects.filter(
                groups=cliente_group)
        else:
            # Si el proyecto ya tiene un ID (es decir, está siendo actualizado), desactivar el campo de cliente
            self.fields['cliente'].disabled = True
        # Initialize habitacion and objeto fields with the current values
        self.fields['habitacion'].initial = json.dumps(self.instance.unityproyect.get('habitacion', ''), indent=4)
        self.fields['objeto'].initial = json.dumps(self.instance.unityproyect.get('objeto', ''), indent=4)