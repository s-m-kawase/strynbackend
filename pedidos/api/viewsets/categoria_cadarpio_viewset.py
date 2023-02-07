from rest_framework import generics, serializers, viewsets
from pedidos.models import CategoriaCardapio
from ..serializers.categoria_cardapio_serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CategoriaCardapioViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = CategoriaCardapio.objects.all()
    serializer_class = CategoriaCardapioSerializer