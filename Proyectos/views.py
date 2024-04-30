from django.shortcuts import render

# Create your views here.
from .models import Categoria

def ver_imagen(request):
    categorias = Categoria.objects.all()
    return render(request, 'proyecto/ver_imagen.html', {'categorias': categorias})