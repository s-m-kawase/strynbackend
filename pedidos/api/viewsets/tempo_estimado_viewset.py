from rest_framework import viewsets, filters
import django_filters.rest_framework
from pedidos.models import TempoEstimado
from ..serializers.tempo_estimado_serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class TempoEstimadoViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = TempoEstimado.objects.all()
    serializer_class = TempoEstimadoSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['tempo']

    search_fields = ['tempo']