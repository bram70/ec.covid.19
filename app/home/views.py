from django.shortcuts import render
from django.http import HttpResponse
from .models import Pregunta, Opcion 
from .serializers import PreguntaSerializer, RespuestaSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .forms import MyGeoForm
import json
#from .forms import CrearCuestionario

def home(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MyGeoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print(form.data)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MyGeoForm()
        cuestionario = Pregunta.objects.values('pregunta_texto', 'pregunta__opcion_texto') 
        for pregunta in cuestionario:
            print(pregunta["pregunta_texto"])
        queryset = Pregunta.objects.all()
        cuestionario_serializer = PreguntaSerializer(queryset, many=True)
        print(json.dumps(cuestionario_serializer.data))
        context = {'form': form, 'cuestionario': cuestionario_serializer.data}
        return render(request, 'home/index.html', context)

class RespuestasView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            respuesta_serializer = RespuestaSerializer(data=request.data)
            if respuesta_serializer.is_valid():
                #Se guarda el modelo
                respuesta = respuesta_serializer.save()

                #Se serializa el objeto creado
                serializer = RespuestaSerializer(instance=respuesta)
                diccionario_respuesta = {
                    'status': status.HTTP_201_CREATED,
                    'data': serializer.data
                }
                return Response(diccionario_respuesta, status=status.HTTP_201_CREATED)
            else:
                diccionario_respuesta = {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': respuesta_serializer.errors,
                    'data': {}
                }
                return Response(diccionario_respuesta, status=status.HTTP_400_BAD_REQUEST)
        except (KeyError, IndexError, ValueError) as e:
            diccionario_respuesta = {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': str(e),
                    'data': {}
                }
            return Response(diccionario_respuesta, status=status.HTTP_400_BAD_REQUEST)