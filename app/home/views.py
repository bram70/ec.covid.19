from django.shortcuts import render
from django.http import HttpResponse
from .models import Pregunta, Opcion 
from .serializers import PreguntaSerializer, RespuestaSerializer, DatosPersonalesSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json
#from .forms import CrearCuestionario

def home(request):
    if request.method == 'GET':
        return render(request, 'home/index.html')

def encuesta(request):
    if request.method == 'GET':
        queryset = Pregunta.objects.all()
        cuestionario_serializer = PreguntaSerializer(queryset, many=True)
        print(json.dumps(cuestionario_serializer.data))
        context = {'cuestionario': cuestionario_serializer.data}
        return render(request, 'home/encuesta.html', context)

class PreguntasView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Pregunta.objects.all()
        cuestionario_serializer = PreguntaSerializer(queryset, many=True)
        diccionario_respuesta = {
            'status': status.HTTP_200_OK,
            'data': cuestionario_serializer.data
        }
        return Response(diccionario_respuesta, status=status.HTTP_200_OK)

class DatosPersonalesView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            datos_serializer = DatosPersonalesSerializer(data=request.data)
            if datos_serializer.is_valid():
                #Se guarda el modelo
                datos_personales = datos_serializer.save()

                #Se serializa el objeto creado
                serializer = DatosPersonalesSerializer(instance=datos_personales)
                diccionario_respuesta = {
                    'status': status.HTTP_201_CREATED,
                    'data': serializer.data
                }
                return Response(diccionario_respuesta, status=status.HTTP_201_CREATED)
            else:
                diccionario_respuesta = {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': datos_serializer.errors,
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