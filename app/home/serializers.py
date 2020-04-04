from .models import Pregunta, Respuesta
from rest_framework import serializers

class PreguntaSerializer(serializers.ModelSerializer):
    opciones = serializers.ReadOnlyField()

    class Meta:
        model = Pregunta
        fields = [
            'id',
            'pregunta_texto',
            'opciones',
            'tipo_input'
        ]

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = "__all__"