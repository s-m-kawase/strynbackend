from rest_framework import serializers 
from pedidos.models import Cardapio

class CardapioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cardapio
        fields = '__all__'