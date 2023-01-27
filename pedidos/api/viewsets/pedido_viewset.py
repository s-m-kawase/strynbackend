from rest_framework import generics, serializers, viewsets 
from pedidos.models import Pedidos  
from ..serializers.pedido_serializer import *


class PedidosViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Pedidos.objects.all()
    serializer_class = PedidosSerializer