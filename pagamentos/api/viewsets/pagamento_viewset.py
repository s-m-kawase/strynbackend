from rest_framework import viewsets, filters
import django_filters.rest_framework
from pagamentos.models import Pagamento
from ..serializers.pagamento_serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PagamentoViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['pagamento']

    search_fields = ['valor_pago']