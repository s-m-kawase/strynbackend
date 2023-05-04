from rest_framework import serializers 
from ...models.ordem_categoria_cardapio import OrdemCategoriaCardapio


class OrdemCategoriaCardapioSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdemCategoriaCardapio
        fields = '__all__'