from rest_framework import generics, serializers, viewsets
from pagamentos.models import Pagamento
from ..serializers.pagamento_serializers import *


class PagamentoViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer