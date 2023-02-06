from rest_framework import serializers 
from pagamentos.models import Pagamento
from pedidos.api.serializers.pedido_serializer import PedidosSerializer


class PagamentoSerializer(serializers.ModelSerializer):
    # property
    total = serializers.ReadOnlyField()
    pedido_read = serializers.SerializerMethodField()
        
    def get_pedido_read(self, obj):
        return PedidosSerializer(instance=obj.pedido).data 

    class Meta:
        model = Pagamento
        fields = '__all__'
