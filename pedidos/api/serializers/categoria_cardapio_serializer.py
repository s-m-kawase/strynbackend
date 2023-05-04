from rest_framework import serializers 
from pedidos.models import CategoriaCardapio
from .ordem_categoria_serializers import OrdemCategoriaCardapioSerializer
from pedidos.models.ordem_categoria_cardapio import OrdemCategoriaCardapio



class CategoriaCardapioSerializer(serializers.ModelSerializer):
    ordens = serializers.SerializerMethodField()

    class Meta:
        model = CategoriaCardapio
        fields = '__all__'

    def get_ordens(self, obj):
        ordens = OrdemCategoriaCardapio.objects.filter(categoria=obj).order_by('ordem')
        return OrdemCategoriaCardapioSerializer(ordens, many=True).data