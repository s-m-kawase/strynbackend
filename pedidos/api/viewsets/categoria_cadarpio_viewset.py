from rest_framework import viewsets, filters
import django_filters.rest_framework
from pedidos.models.cardapio import Cardapio
from pedidos.models import CategoriaCardapio
from ..serializers.categoria_cardapio_serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CategoriaCardapioViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = CategoriaCardapio.objects.all()
    serializer_class = CategoriaCardapioSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['status','restaurante']

    search_fields = ['nome']

    def get_queryset(self):
        query = super().get_queryset()
        if self.request.GET.get("meus_cardapios",False):
            usuario = self.request.user
            cardapios = Cardapio.objects.filter(restaurante__usuario=usuario)
            ids_categorias = []
            for cardapio in cardapios:
                for categoria in cardapio.categorias.all():
                    ids_categorias.append(categoria.id)
            ids_categorias = list(set(ids_categorias))

            query = query.filter(id__in=ids_categorias).distinct()
        
        return query