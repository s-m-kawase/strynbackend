from rest_framework import generics, serializers, viewsets
from pedidos.models import ItensPedido
from ..serializers.item_pedido_serializer import *
from rest_framework.permissions import IsAuthenticated


class ItensPedidoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ItensPedido.objects.all()
    serializer_class = ItensPedidoSerializer
   