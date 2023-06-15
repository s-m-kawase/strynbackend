from rest_framework import serializers
from pedidos.models import Restaurante
from .tempo_estimado_serializer import TempoEstimadoSerializer


class RestauranteSerializer(serializers.ModelSerializer):

    tempo_estimado_read = serializers.SerializerMethodField()

    def get_tempo_estimado_read(self, obj):
        return [TempoEstimadoSerializer(instance=obj.tempo_estimado).data] if obj.tempo_estimado else None
    class Meta:
        model = Restaurante
        fields = '__all__'