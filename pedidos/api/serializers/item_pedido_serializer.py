from rest_framework import serializers 
from pedidos.models import ItensPedido
from .pedido_serializer import PedidosSerializer
from .item_cardapio_serializer import ItemCardapioSerializer
class ItensPedidoSerializer(serializers.ModelSerializer):
    item_read = serializers.SerializerMethodField()
    pedido_read = serializers.SerializerMethodField()

    def get_item_read(self, obj):
        return ItemCardapioSerializer(obj.item).data if obj.item else None
    
    def get_pedido_read(self, obj):
        return PedidosSerializer(obj.pedido).data if obj.pedido else None
    class Meta:
        model = ItensPedido
        fields = '__all__'