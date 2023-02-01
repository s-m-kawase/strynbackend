from rest_framework import generics, serializers, viewsets
from pedidos.models import CategoriaCardapio
from ..serializers.categoria_cardapio_serializer import *
from rest_framework.permissions import IsAuthenticated


class CategoriaCardapioViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CategoriaCardapio.objects.all()
    serializer_class = CategoriaCardapioSerializer