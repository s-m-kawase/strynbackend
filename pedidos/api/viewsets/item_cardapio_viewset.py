from rest_framework import generics, serializers, viewsets
from pedidos.models import ItemCardapio
from ..serializers.item_cardapio_serializer import *
from rest_framework.permissions import IsAuthenticated



class ItemCardapioViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ItemCardapio.objects.all()
    serializer_class = ItemCardapioSerializer