from rest_framework import generics, serializers, viewsets
from pedidos.models import CategoriaCardapio
from ..serializers.categoria_cardapio_serializer import *


class CategoriaCardapioViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = CategoriaCardapio.objects.all()
    serializer_class = CategoriaCardapioSerializer