from rest_framework import generics, serializers, viewsets
from pedidos.models import Item
from ..serializers.item_serializer import *


class ItemViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Item.objects.all()
    serializer_class = ItemSerializer