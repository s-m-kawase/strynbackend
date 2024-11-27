from rest_framework import viewsets, filters
import django_filters.rest_framework
from pedidos.models import ItensPedido
from ..serializers.item_pedido_serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ItensPedidoViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = ()
    queryset = ItensPedido.objects.all()
    serializer_class = ItensPedidoSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['quantidade','item','pedido']

    search_fields = ['item__name']
