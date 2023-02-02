from rest_framework import serializers 
from pagamentos.models import Adicional


class AdicionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adicional
        fields = '__all__'