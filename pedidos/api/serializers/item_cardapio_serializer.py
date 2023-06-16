from rest_framework import serializers
from pedidos.models import ItemCardapio
from .categoria_cardapio_serializer import CategoriaCardapioSerializer
from .grupo_complemento_item_serializer import GrupoComplementosSerializer


class ItemCardapioSerializer(serializers.ModelSerializer):
    # property
    promocao = serializers.ReadOnlyField()
    categoria_read = serializers.SerializerMethodField()
    grupo_complemento_read = serializers.SerializerMethodField()
    
    def get_grupo_complemento_read(self, obj):
        return [GrupoComplementosSerializer(instance=grupo_complemento).data for grupo_complemento in obj.grupo_complemento.all()]

    def get_categoria_read(self, obj):
        return [CategoriaCardapioSerializer(instance=categoria).data for categoria in obj.categoria.all()]

    class Meta:
        model = ItemCardapio
        fields = '__all__'

