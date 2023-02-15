from rest_framework import viewsets , filters
import django_filters.rest_framework
from pedidos.models import ItemCardapio
from ..serializers.grupo_complemento_item_serializer import GrupoComplementosSerializer
from ..serializers.item_cardapio_serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.http.response import JsonResponse

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ItemCardapioViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = ItemCardapio.objects.all()
    serializer_class = ItemCardapioSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['tamanho_fome','status_venda']

    search_fields = ['nome','preco']

    @action(methods=['get'], detail=True)
    def complemento(self, request, pk):
        item_cardapio = self.get_object()
        grupo_complementos = item_cardapio.grupo_complemento.all()

        # Faça algo com cada grupo de complementos associado a este item de cardápio
        relatorio_complementos = []
        for grupo_complemento in grupo_complementos:
            nome= []
            for complemento in grupo_complemento.complemento.all():
                nome.append({
                    "nome_complementos":complemento.nome
                })
            relatorio_complementos.append({
                "complemento":nome,
                "Obrigatorio": grupo_complemento.obrigatoriedade,
                "objeto":GrupoComplementosSerializer(instance=grupo_complemento).data
            })

        context = {
            "relatorio_complemento": relatorio_complementos,
            
        }

        return JsonResponse(
            context,
            content_type="application/json"
        )



