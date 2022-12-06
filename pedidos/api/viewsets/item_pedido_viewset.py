from rest_framework import generics, serializers, viewsets
from pedidos.models import IntensPedido
from ..serializers.item_pedido_serializer import *


class IntensPedidoViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = IntensPedido.objects.all()
    serializer_class = IntensPedidoSerializer
   