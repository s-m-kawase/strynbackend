from rest_framework import serializers
from pedidos.models import ItensPedidoComplementos


class ItensPedidoComplementosSerializer(serializers.ModelSerializer):
    total=serializers.ReadOnlyField()
    class Meta:
        model = ItensPedidoComplementos
        fields = '__all__'
