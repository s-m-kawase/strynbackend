from rest_framework import generics, serializers, viewsets
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
    permission_classes = (IsAuthenticated,)
    queryset = ItensPedido.objects.all()
    serializer_class = ItensPedidoSerializer
   