from rest_framework import generics, serializers, viewsets
from pedidos.models import Restaurante
from ..serializers.restaurante_serializer import *


class RestauranteViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Restaurante.objects.all()
    serializer_class = RestauranteSerializer