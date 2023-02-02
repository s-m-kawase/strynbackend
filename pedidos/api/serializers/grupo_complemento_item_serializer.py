from rest_framework import serializers 
from pedidos.models import GrupoComplementos

from .complemento_serializer import ComplementosSerializer


class GrupoComplementosSerializer(serializers.ModelSerializer):
    complemento = ComplementosSerializer()
    class Meta:
        model = GrupoComplementos
        fields = '__all__'
