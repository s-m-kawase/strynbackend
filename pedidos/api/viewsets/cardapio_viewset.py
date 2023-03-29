from rest_framework import viewsets, filters
import django_filters.rest_framework
from pedidos.models import Cardapio
from ..serializers.cardapio_serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CardapioViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = Cardapio.objects.all()
    serializer_class = CardapioSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['restaurante']

    search_fields = ['nome']

    def get_queryset(self):
        query = super().get_queryset()

        usuario = self.request.user
        query = query.filter(restaurante__usuario=usuario)

        return query