from rest_framework import serializers 
from pedidos.models import ItensPedido


class ItensPedidoSerializer((serializers.ModelSerializer)):
    class Meta:
        model = ItensPedido
        fields = '__all__'