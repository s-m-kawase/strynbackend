from rest_framework import generics, serializers, viewsets
from pedidos.models import ItemCardapio
from ..serializers.item_serializer import *


class ItemCardapioViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = ItemCardapio.objects.all()
    serializer_class = ItemCardapioSerializer