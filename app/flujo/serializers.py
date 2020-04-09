from rest_framework import serializers
from .models import Flujo, Proceso

class FlujoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flujo
        fields = "__all__"

class ProcesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proceso
        fields = "__all__"