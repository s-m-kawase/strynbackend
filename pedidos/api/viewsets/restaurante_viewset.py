from rest_framework import generics, serializers, viewsets
from pedidos.models import Restaurante
from ..serializers.restaurante_serializer import *
from rest_framework.permissions import IsAuthenticated



class RestauranteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Restaurante.objects.all()
    serializer_class = RestauranteSerializer