from rest_framework import generics, serializers, viewsets
from pedidos.models import Cardapio
from ..serializers.cardapio_serializers import *


class CardapioViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Cardapio.objects.all()
    serializer_class = CardapioSerializer