from rest_framework import generics, serializers, viewsets 
from pedidos.models import Pedidos  
from ..serializers.pedido_serializer import *
from rest_framework.permissions import IsAuthenticated



class PedidosViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Pedidos.objects.all()
    serializer_class = PedidosSerializer