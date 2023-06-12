from rest_framework import serializers
from pagamentos.models import Pagamento
from pedidos.api.serializers.pedido_serializer import PedidosSerializer


class PagamentoSerializer(serializers.ModelSerializer):
    # property
    total = serializers.ReadOnlyField()

    class Meta:
        model = Pagamento
        fields = '__all__'
