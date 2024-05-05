from django.shortcuts import render

from .models import Proyecto
from django.contrib.auth.decorators import login_required

@login_required
def listar_proyectos(request):
    proyectos = Proyecto.objects.filter(diseñador=request.user)
    return render(request, 'proyecto/listar_proyectos.html', {'proyectos': proyectos})
