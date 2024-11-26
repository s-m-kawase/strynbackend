from rest_framework import serializers
from pedidos.models import Cardapio
from .ordem_categoria_serializers import OrdemCategoriaCardapioSerializer
from .restaurante_serializer import RestauranteSerializer
from pedidos.models.ordem_categoria_cardapio import OrdemCategoriaCardapio


class CardapioComOrdemSerializer(serializers.ModelSerializer):
    ordens = serializers.SerializerMethodField()
    restaurante_read = serializers.SerializerMethodField()
    
    def get_restaurante_read(self,obj):
        return RestauranteSerializer(instance=obj.restaurante).data

    def get_ordens(self, obj):
        ordens = OrdemCategoriaCardapio.objects.filter(cardapio=obj).order_by('ordem')
        return OrdemCategoriaCardapioSerializer(ordens, many=True).data


    class Meta:
        model = Cardapio
        fields = '__all__'