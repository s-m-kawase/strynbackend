from rest_framework import serializers 
from pedidos.models import IntensPedido


class IntensPedidoSerializer((serializers.ModelSerializer)):
    class Meta:
        model = IntensPedido
        fields = '__all__'