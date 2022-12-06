from rest_framework import serializers 
from pedidos.models import Complementos


class ComplementosSerializer((serializers.ModelSerializer)):
    class Meta:
        model = Complementos
        fields = '__all__'
