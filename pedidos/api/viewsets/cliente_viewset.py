from rest_framework import generics, serializers, viewsets
from pedidos.models import Cliente
from ..serializers.cliente_serializers import *


class ClienteViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer