from rest_framework import viewsets, filters, permissions
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny
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


class CardapioViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrReadOnly]
    queryset = Cardapio.objects.all()
    serializer_class = CardapioSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['restaurante']

    search_fields = ['nome']



    def get_queryset(self):
        query = super().get_queryset()
        parametro = self.request.query_params
        cardapio = parametro.get('cardapio',None)
        restaurante = parametro.get('restaurante',None)

        # Verifica se o usuário é anônimo
        if self.request.user.is_authenticated:
            if cardapio:
                query = query.filter(id=cardapio)
            else:
              usuario = self.request.user
              print(usuario)
              query = query.filter(restaurante__usuario=usuario)


        elif self.request.user.is_anonymous:
            if cardapio and restaurante:
              query = query.filter(
                  id=cardapio,
                  restaurante=restaurante
              )


        return query