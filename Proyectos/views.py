from django.shortcuts import render, redirect, get_object_or_404

from .models import Proyecto
from .forms import ProyectoForm
from django.contrib.auth.decorators import login_required

@login_required
def listar_proyectos(request):
    usuario = request.user
    if usuario.groups.filter(name='Diseñador').exists():  # Verifica si el usuario pertenece al grupo Diseñadores
        proyectos = Proyecto.objects.filter(diseñador=request.user)
    else:
        proyectos = Proyecto.objects.filter(cliente=request.user)
    return render(request, 'proyecto/listar_proyectos.html', {'proyectos': proyectos, 'usuario': usuario})


@login_required
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.diseñador = request.user
            proyecto.save()
            return redirect('index')
    else:
        form = ProyectoForm()
    return render(request, 'proyecto/crear_proyecto.html', {'form': form})

@login_required
def actualizar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'proyecto/actualizar_proyecto.html', {'form': form})


@login_required
def eliminar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    proyecto.delete()
    return redirect('index')
