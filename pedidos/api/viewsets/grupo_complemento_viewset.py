from rest_framework import viewsets , filters
import django_filters.rest_framework
from pedidos.models import GrupoComplementos
from ..serializers.grupo_complemento_item_serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class GrupoComplementosViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = GrupoComplementos.objects.all()
    serializer_class = GrupoComplementosSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['obrigatoriedade','quantidade_minima','quantidade_maxima']

    search_fields = ['nome']
    
    def get_queryset(self):
        query = super().get_queryset()
        usuario = self.request.user.id
        #usuario = usuario.get_username()
        query = query.filter(cardapio__restaurante__usuario=usuario).distinct()

        return query