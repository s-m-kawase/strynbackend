from rest_framework import generics, serializers, viewsets
from pedidos.models import ItensPedidoComplementos
from ..serializers.item_pedido_complemento_serializer import *


class ItensPedidoComplementosViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = ItensPedidoComplementos.objects.all()
    serializer_class = ItensPedidoComplementosSerializer