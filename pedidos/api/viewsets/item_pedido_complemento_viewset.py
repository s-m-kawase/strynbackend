from rest_framework import generics, serializers, viewsets
from pedidos.models import ItensPedidoComplementos
from ..serializers.item_pedido_complemento_serializer import *
from rest_framework.permissions import IsAuthenticated



class ItensPedidoComplementosViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ItensPedidoComplementos.objects.all()
    serializer_class = ItensPedidoComplementosSerializer