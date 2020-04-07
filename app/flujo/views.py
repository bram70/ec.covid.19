from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from home.models import Pregunta, Opcion 
from home.serializers import PreguntaSerializer, RespuestaSerializer
from .types import FLUJO_CONDICIONAL, FLUJO_FIN, FLUJO_INICIO, FLUJO_NORMAL
from .models import Flujo
from .serializers import FlujoSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json

# Create your views here.
def obtenerListaPreguntas(flujo_pregunta_inicial:Flujo):
    if isinstance(flujo_pregunta_inicial, Flujo) :
        # Se inicializa la lista de preguntas a retornar 
        preguntas_mostradas = []
        #Se serializa y guarda la pregunta inicial dada en la lista
        pregunta_inicial_serializada = PreguntaSerializer(instance=flujo_pregunta_inicial.pregunta)
        preguntas_mostradas.append(pregunta_inicial_serializada.data)

        #se setea la el flujo de la pregunta inicial como la el flujo actual
        flujo_pregunta = flujo_pregunta_inicial

        # Mientras que la pregunta actual no sea un final de seccion
        # y tenga una pregunta siguiente en el flujo se guarda 
        # la siguiente pregunta en la lista
        while flujo_pregunta.fin_de_seccion == 0 and flujo_pregunta.siguiente_pregunta_en_flujo is not None:
            # se setea como flujo actual la siguiente pregunta
            flujo_pregunta = flujo_pregunta.siguiente_pregunta_en_flujo

            #Se serializa y guarda la pregunta actual en la lista
            pregunta_serializada = PreguntaSerializer(instance=flujo_pregunta.pregunta)
            preguntas_mostradas.append(pregunta_serializada.data)

        return preguntas_mostradas
    else:
        raise ValueError

class IniciarFlujoView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            #Se obtiene la pregunta inicial del flujo
            queryset = Flujo.objects.get(tipo_flujo__exact=FLUJO_INICIO)
            
            #Se obtiene la lista de preguntas siguientes a partir del flujo inicial
            lista_preguntas = obtenerListaPreguntas(queryset)

            diccionario_respuesta = {
                'status': status.HTTP_200_OK,
                'data': lista_preguntas
            }
            return Response(diccionario_respuesta, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, ValueError) as e:
            diccionario_respuesta = {
                'status': status.HTTP_404_NOT_FOUND,
                'message': str(e),
                'data': {}
            }
            return Response(diccionario_respuesta, status=status.HTTP_400_BAD_REQUEST)
