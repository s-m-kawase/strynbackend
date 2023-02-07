from rest_framework import generics, serializers, viewsets
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