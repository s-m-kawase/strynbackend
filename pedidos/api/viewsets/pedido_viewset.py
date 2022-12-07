from rest_framework import generics, serializers, viewsets 
from pedidos.models import Pedido  
from ..serializers.pedido_serializer import *


class PedidoViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer