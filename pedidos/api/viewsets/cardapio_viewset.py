from rest_framework import viewsets, filters, permissions
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser
import django_filters.rest_framework
from pedidos.models import Cardapio
from ..serializers.cardapio_serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user and request.user.is_superuser


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return IsAuthenticated().has_permission(request, view)
class CardapioViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrReadOnly]
    queryset = Cardapio.objects.all()
    serializer_class = CardapioSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['restaurante']

    search_fields = ['nome']

    def get_permissions(self):
        if self.request.user.is_superuser:
            permission_classes = [IsAdminOrReadOnly]
        elif self.request.user.is_authenticated:
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]  # Permitir acesso não autenticado

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        query = super().get_queryset()

        usuario = self.request.user
        query = query.filter(restaurante__usuario=usuario)

        return query