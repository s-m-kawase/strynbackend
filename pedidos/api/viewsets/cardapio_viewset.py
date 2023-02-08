from rest_framework import generics, serializers, viewsets
from pedidos.models import Cardapio
from ..serializers.cardapio_serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CardapioViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = Cardapio.objects.all()
    serializer_class = CardapioSerializer