from rest_framework import viewsets, filters
import django_filters.rest_framework
from pedidos.models import Cliente
from ..serializers.cliente_serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ClienteViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    # permission_classes = (IsAuthenticated,)
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = []

    search_fields = ['nome_cliente']