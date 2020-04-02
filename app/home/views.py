from django.shortcuts import render
from django.http import HttpResponse
from .models import Pregunta, Opcion 
#from .forms import CrearCuestionario

def home(request):
    cuestionario = Pregunta.objects.values('pregunta_texto', 'pregunta__opcion_texto') 
    context = {'cuestionario': cuestionario}
    return render(request, 'home/index.html', context)
