from rest_framework import serializers
from pedidos.models import TempoEstimado


class TempoEstimadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempoEstimado
        fields = '__all__'