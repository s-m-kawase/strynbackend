from rest_framework import generics, serializers, viewsets
from pedidos.models import Cardapio
from ..serializers.cardapio_serializers import *
from rest_framework.permissions import IsAuthenticated


class CardapioViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Cardapio.objects.all()
    serializer_class = CardapioSerializer