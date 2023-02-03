from rest_framework import serializers 
from pedidos.models import Pedidos

from .cliente_serializers import ClienteSerializer
from .tempo_estimado_serializer import TempoEstimadoSerializer

class PedidosSerializer(serializers.ModelSerializer):
    #  property
    total = serializers.ReadOnlyField()
    subtotal_read = serializers.ReadOnlyField()
    
    cliente_read = serializers.SerializerMethodField()
    tempo_estimado_read = serializers.SerializerMethodField()
    

    def get_tempo_estimado_read(self, obj):
         return [TempoEstimadoSerializer(instance=tempo_estimado).data for tempo_estimado in obj.tempo_estimado.all()]


    def get_cliente_read(self, obj):    
        return ClienteSerializer(instance=obj.cliente).data

    class Meta:
        model = Pedidos
        fields = '__all__'