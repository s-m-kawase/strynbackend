from rest_framework import serializers
from pagamentos.models import Cupom
class CupomSerializer(serializers.ModelSerializer):
    status_cupom = serializers.ReadOnlyField()
    class Meta:
        model = Cupom
        fields = '__all__'
