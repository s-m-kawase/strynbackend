from rest_framework import serializers 
from pedidos.models import ItemCardapio
from .categoria_cardapio_serializer import CategoriaCardapioSerializer


class ItemCardapioSerializer((serializers.ModelSerializer)):
    categoria = CategoriaCardapioSerializer()
    class Meta:
        model = ItemCardapio
        fields = '__all__'

