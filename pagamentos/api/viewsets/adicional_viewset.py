from rest_framework import viewsets, filters
import django_filters.rest_framework
from pagamentos.models import Adicional
from ..serializers.adicional_serializers import *

from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class AdicionalViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = Adicional.objects.all()
    serializer_class = AdicionalSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['valor']

    search_fields = ['nome','valor']