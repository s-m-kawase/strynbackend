from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from ...models import Cardapio
from ..serializers.cardapio_com_ordem_serializer import CardapioComOrdemSerializer


class CardapioComOrdemViewSet(viewsets.ModelViewSet):
    queryset = Cardapio.objects.all()
    serializer_class = CardapioComOrdemSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]

    search_fields = [
        
    ]
