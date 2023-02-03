from rest_framework import serializers 
from pedidos.models import GrupoComplementos

from .complemento_serializer import ComplementosSerializer


class GrupoComplementosSerializer(serializers.ModelSerializer):
    complemento_read = serializers.SerializerMethodField()
    
    def get_complemento_read(self, obj):
        return [GrupoComplementosSerializer(instance=complemento).data for complemento in obj.complemento.all()]
    class Meta:
        model = GrupoComplementos
        fields = '__all__'
