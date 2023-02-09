from rest_framework import viewsets , filters
import django_filters.rest_framework
from pedidos.models import ItemCardapio
from ..serializers.item_cardapio_serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ItemCardapioViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = ItemCardapio.objects.all()
    serializer_class = ItemCardapioSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['tamanho_fome','status_venda']

    search_fields = ['nome','preco']