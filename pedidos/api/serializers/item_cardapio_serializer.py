from rest_framework import serializers 
from pedidos.models import ItemCardapio
from .categoria_cardapio_serializer import CategoriaCardapioSerializer
from .grupo_complemento_item_serializer import GrupoComplementosSerializer


class ItemCardapioSerializer((serializers.ModelSerializer)):
    categoria_get = serializers.SerializerMethodField()
    grupo_complemento=GrupoComplementosSerializer()

    def get_categoria_get(self, obj):
        return CategoriaCardapioSerializer(instance=obj.categoria).data if obj.categoria else None
    
    class Meta:
        model = ItemCardapio
        fields = '__all__'

