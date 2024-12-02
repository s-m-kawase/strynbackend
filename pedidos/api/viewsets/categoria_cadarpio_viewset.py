from rest_framework import viewsets, filters
import django_filters.rest_framework
from rest_framework.permissions import BasePermission
from pedidos.models.cardapio import Cardapio
from pedidos.models import CategoriaCardapio
from ..serializers.categoria_cardapio_serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user and request.user.is_superuser

class CategoriaCardapioViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAdminOrReadOnly,)
    queryset = CategoriaCardapio.objects.all()
    serializer_class = CategoriaCardapioSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['status','restaurante','cardapio', 'restaurante__slug']

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

            query = query.filter(id__in=ids_categorias)
        
        return query
    
    @action(methods=['get', 'post'], detail=False)
    def ordenacao(self, request):
        
        item_cardapio = request.data.getlist('itemcardapios', [])
    
        for i, item in enumerate(item_cardapio):
            
            item_cardapio[i] = int(item)
        context = {
            
        }

        return Response(
            context
        )