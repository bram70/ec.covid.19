from rest_framework import serializers
from .models import Flujo

class FlujoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flujo
        fields = "__all__"