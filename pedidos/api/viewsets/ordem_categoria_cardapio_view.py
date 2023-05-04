from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from ...models.ordem_categoria_cardapio import OrdemCategoriaCardapio
from ..serializers.ordem_categoria_serializers import OrdemCategoriaCardapioSerializer


class OrdemCategoriaCardapioViewSet(viewsets.ModelViewSet):
    queryset = OrdemCategoriaCardapio.objects.all()
    serializer_class = OrdemCategoriaCardapioSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]

    search_fields = [
        
    ]
