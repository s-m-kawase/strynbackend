from rest_framework import serializers 
from pedidos.models import Cardapio
from .ordem_categoria_serializers import OrdemCategoriaCardapioSerializer
from pedidos.models.ordem_categoria_cardapio import OrdemCategoriaCardapio


class CardapioComOrdemSerializer(serializers.ModelSerializer):
    ordens = serializers.SerializerMethodField()
   
    def get_ordens(self, obj):
        ordens = OrdemCategoriaCardapio.objects.filter(cardapio=obj).order_by('ordem')
        return OrdemCategoriaCardapioSerializer(ordens, many=True).data
    

    class Meta:
        model = Cardapio
        fields = '__all__'