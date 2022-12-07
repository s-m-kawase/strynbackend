from rest_framework import serializers 
from pagamentos.models import Pagamento


class PagamentoSerializer((serializers.ModelSerializer)):
    class Meta:
        model = Pagamento
        fields = '__all__'
