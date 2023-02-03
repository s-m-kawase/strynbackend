from rest_framework import serializers
from pedidos.models import ItensPedidoComplementos
from .item_pedido_serializer import ItensPedidoSerializer
from .complemento_serializer import ComplementosSerializer


class ItensPedidoComplementosSerializer(serializers.ModelSerializer):
    # property
    total = serializers.ReadOnlyField()

    complemento_read = serializers.SerializerMethodField()
    item_pedido_read = serializers.SerializerMethodField()

    def get_item_pedido_read(self,obj):
        return ItensPedidoSerializer(instance=obj.item_pedido).data

    def get_complemento_read(self,obj):
        return ComplementosSerializer(instance=obj.complemento).data

    class Meta:
        model = ItensPedidoComplementos
        fields = '__all__'
