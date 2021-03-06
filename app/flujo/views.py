from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from home.models import Pregunta, Opcion 
from home.serializers import PreguntaSerializer, RespuestaSerializer
from .types import FLUJO_CONDICIONAL, FLUJO_FIN, FLUJO_INICIO, FLUJO_NORMAL
from .models import Flujo, Proceso
from .serializers import FlujoSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json
from django.contrib.gis.geoip2 import GeoIP2
from home.types import CIUDAD_DEFAULT, DEFAULT_DIRECCION_WKT, UBICACION_DEFAULT_EN_MODELO

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


        #Se crea el diccionario de respuesta con los siguientes flujos en null
        diccionario_respuesta = {
            "siguiente_pregunta_en_flujo": None,
            "siguiente_pregunta_en_flujo_negativo" : None,
            "id_opcion_positiva": None,
            "preguntas": preguntas_mostradas
        }

        if flujo_pregunta.siguiente_pregunta_en_flujo is not None:
            diccionario_respuesta["siguiente_pregunta_en_flujo"] = flujo_pregunta.siguiente_pregunta_en_flujo.id

        if flujo_pregunta.es_condicional == 1 and flujo_pregunta.siguiente_pregunta_en_flujo_negativo is not None:
            diccionario_respuesta["siguiente_pregunta_en_flujo_negativo"] = flujo_pregunta.siguiente_pregunta_en_flujo_negativo.id

        if flujo_pregunta.es_condicional == 1:
            pregunta = flujo_pregunta.pregunta
            opcion_positiva = Opcion.objects.get(pregunta__exact= pregunta.id, es_positiva__exact=1)
            id_opcion_positiva = opcion_positiva.id
            diccionario_respuesta["id_opcion_positiva"] = id_opcion_positiva

        return diccionario_respuesta
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

class ObtenerPreguntasSiguientes(APIView):
    def get(self, request, *args, **kwargs):
        try:
            flujo_pk = self.kwargs['pk']
            #Se obtiene la pregunta inicial del flujo
            queryset = Flujo.objects.get(pk=flujo_pk)
            
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

class EnviarRespuestasView(APIView):
    def post(self, request, *args, **kwargs):
        #Este metodo espera una lista de respuestas.
        respuesta_serializer = RespuestaSerializer(data=request.data, many=True)
        print(request.data)

        if respuesta_serializer.is_valid():
            #print(respuesta_serializer.validated_data)
            data = respuesta_serializer.save()

            #Se obtiene la ubicación a partir de la ip
            ubicacion = obtener_lat_long_de_ciudad_wkt_con_request(request)
            print(ubicacion)

            for respuesta in data:
                if(respuesta.location == UBICACION_DEFAULT_EN_MODELO):
                    print("era default")
                    respuesta.location = "SRID=4326;"+ubicacion
                    respuesta.save()

                

            repuestas_guardadas = RespuestaSerializer(data, many=True)
            diccionario_respuesta = {
                'status': status.HTTP_201_CREATED,
                'data': repuestas_guardadas.data
            }
            return Response(diccionario_respuesta, status=status.HTTP_201_CREATED)
        else: 
            diccionario_respuesta = {
                'status': status.HTTP_404_NOT_FOUND,
                'message': respuesta_serializer.errors,
                'data': {}
            }
        return Response(diccionario_respuesta, status=status.HTTP_400_BAD_REQUEST)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        print("primera opcion")
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
        print("segunda opcion")
    return ip

def obtener_lat_long_de_ciudad_wkt(ip):
    try: 
        g = GeoIP2()
        location = g.lat_lon(ip)
        return "POINT(" +str(location[0])+" "+ str(location[1])+")"
    except Exception as e:
        print("Exception here")
        print(str(e))
        return DEFAULT_DIRECCION_WKT

def obtener_lat_long_de_ciudad_wkt_con_request(request):
    try:
        ip = get_client_ip(request)
        return obtener_lat_long_de_ciudad_wkt(ip)
    except Exception as e:
        print("Exception here")
        print(str(e))
        return DEFAULT_DIRECCION_WKT

