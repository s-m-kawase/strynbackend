from rest_framework import serializers 
from pedidos.models import Pedidos
from pagamentos.api.serializers.adicional_serializers import AdicionalSerializer
from pagamentos.api.serializers.cupom_serializers import CupomSerializer

from .cliente_serializers import ClienteSerializer
from .tempo_estimado_serializer import TempoEstimadoSerializer
from .restaurante_serializer import RestauranteSerializer

class PedidosSerializer(serializers.ModelSerializer):
    #  property
    total = serializers.ReadOnlyField()
    subtotal = serializers.ReadOnlyField()
    itens_quantidade = serializers.ReadOnlyField()
    
    adicionais_read = serializers.SerializerMethodField()
    cupom_read = serializers.SerializerMethodField()
    cliente_read = serializers.SerializerMethodField()
    tempo_estimado_read = serializers.SerializerMethodField()
    restaurante_read = serializers.SerializerMethodField()


    def get_adicionais_read(self, obj):
        return [AdicionalSerializer(instance=adicionais).data for adicionais in obj.adicionais.all()]

    def get_cupom_read(self, obj):
        return CupomSerializer(instance=obj.cupom).data if obj.cupom else None

    def get_tempo_estimado_read(self, obj):
         return [TempoEstimadoSerializer(instance=tempo_estimado).data for tempo_estimado in obj.tempo_estimado.all()]

    def get_cliente_read(self, obj):    
        return ClienteSerializer(instance=obj.cliente).data if obj.cliente else None

    def get_restaurante_read(self, obj):    
        return RestauranteSerializer(instance=obj.restaurante).data

    class Meta:
        model = Pedidos
        fields = '__all__'