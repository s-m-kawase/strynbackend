from rest_framework import serializers 
from pedidos.models import CategoriaCardapio



class CategoriaCardapioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaCardapio
        fields = '__all__'
