from rest_framework import serializers 
from pedidos.models import Pedido

from pagamentos.api.serializers.pagamento_serializers import PagamentoSerializer
from pagamentos.api.serializers.cupom_serializers import CupomSerializer
from .cliente_serializers import ClienteSerializer
from .tempo_estimado_serializer import TempoEstimadoSerializer

class PedidoSerializer((serializers.ModelSerializer)):
    pagamento = PagamentoSerializer()
    cupom =CupomSerializer()
    cliente = ClienteSerializer()
    tempo_estimado = TempoEstimadoSerializer()
    class Meta:
        model = Pedido
        fields = '__all__'