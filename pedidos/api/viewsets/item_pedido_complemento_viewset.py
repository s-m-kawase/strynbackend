from rest_framework import viewsets, filters
import django_filters.rest_framework
from pedidos.models import ItensPedidoComplementos
from ..serializers.item_pedido_complemento_serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ItensPedidoComplementosViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = ItensPedidoComplementos.objects.all()
    serializer_class = ItensPedidoComplementosSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['complemento']

    search_fields = ['complemento__nome']