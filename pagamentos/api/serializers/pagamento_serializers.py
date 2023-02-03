from rest_framework import serializers 
from pagamentos.models import Pagamento
from pedidos.api.serializers.pedido_serializer import PedidosSerializer
from .adicional_serializers import AdicionalSerializer
from .cupom_serializers import CupomSerializer


class PagamentoSerializer(serializers.ModelSerializer):
    # property
    total = serializers.ReadOnlyField()

    adicionais_read = serializers.SerializerMethodField()
    cupom_read = serializers.SerializerMethodField()
    pedido_read = serializers.SerializerMethodField()

    def get_adicionais_read(self, obj):
        return [AdicionalSerializer(instance=adicionais).data for adicionais in obj.adicionais.all()]
        
    def get_cupom_read(self, obj):
        return CupomSerializer(instance=obj.cupom).data 
        
    def get_pedido_read(self, obj):
        return PedidosSerializer(instance=obj.pedido).data 

    class Meta:
        model = Pagamento
        fields = '__all__'
