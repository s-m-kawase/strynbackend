from rest_framework import serializers 
from pedidos.models import Cardapio
from .categoria_cardapio_serializer import CategoriaCardapioSerializer
from .restaurante_serializer import RestauranteSerializer

class CardapioSerializer(serializers.ModelSerializer):
    categoria_read = serializers.SerializerMethodField()
    restaurante_read = serializers.SerializerMethodField()

    
    def get_categoria_read(self, obj):
        return [CategoriaCardapioSerializer(instance=categorias).data for categorias in obj.categorias.all()]

    def get_restaurante_read(self,obj):
        return RestauranteSerializer(instance=obj.restaurante).data

    class Meta:
        model = Cardapio
        fields = '__all__'