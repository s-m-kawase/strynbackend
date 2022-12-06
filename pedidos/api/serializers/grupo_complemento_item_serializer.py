from rest_framework import serializers 
from pedidos.models import GrupoComplementos



class GrupoComplementosSerializer((serializers.ModelSerializer)):
    class Meta:
        model = GrupoComplementos
        fields = '__all__'
