from rest_framework import generics, serializers, viewsets
from pedidos.models import ItensPedido
from ..serializers.item_pedido_serializer import *


class ItensPedidoViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = ItensPedido.objects.all()
    serializer_class = ItensPedidoSerializer
   