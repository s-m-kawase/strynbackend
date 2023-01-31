from rest_framework import serializers 
from pedidos.models import ItemCardapio
from .categoria_cardapio_serializer import CategoriaCardapioSerializer
from .grupo_complemento_item_serializer import GrupoComplementosSerializer


class ItemCardapioSerializer((serializers.ModelSerializer)):
    categoria_get = serializers.ReadOnlyField()
    categoria = CategoriaCardapioSerializer()
    grupo_complemento=GrupoComplementosSerializer()

    
    class Meta:
        model = ItemCardapio
        fields = '__all__'

