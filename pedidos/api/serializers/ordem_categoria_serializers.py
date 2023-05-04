from rest_framework import serializers 
from ...models.ordem_categoria_cardapio import OrdemCategoriaCardapio
from .categoria_cardapio_serializer import CategoriaCardapioSerializer


class OrdemCategoriaCardapioSerializer(serializers.ModelSerializer):
    categoria_read = serializers.SerializerMethodField()
    
    def get_categoria_read(self, obj):
        return CategoriaCardapioSerializer(obj.categoria).data
    class Meta:
        model = OrdemCategoriaCardapio
        fields = '__all__'