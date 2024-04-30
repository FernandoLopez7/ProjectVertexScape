from django.shortcuts import render, redirect

# Permisos
from django.contrib.auth.decorators import login_required

from .models import User

# # Para el login 
from django.contrib.auth import login
from .forms import EmailAuthenticationForm, PerfilForm

def iniciar_sesion(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('perfil')  # Reemplaza 'pagina_inicio' con la URL a la que quieres redirigir después del inicio de sesión
    else:
        form = EmailAuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirige al perfil después de guardar los cambios
    else:
        form = PerfilForm(instance=request.user)
    return render(request, 'usuarios/editar_perfil.html', {'form': form})

@login_required
def perfil(request):
    usuario = request.user
    return render(request, 'usuarios/perfil.html', {'usuario': usuario})
