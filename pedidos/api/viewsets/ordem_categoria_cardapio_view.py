from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http.response import JsonResponse
from ...models.ordem_categoria_cardapio import OrdemCategoriaCardapio
from ..serializers.ordem_categoria_serializers import OrdemCategoriaCardapioSerializer


class OrdemCategoriaCardapioViewSet(viewsets.ModelViewSet):
    queryset = OrdemCategoriaCardapio.objects.all()
    serializer_class = OrdemCategoriaCardapioSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]

    search_fields = [
        
    ]


    @action(methods=['get'], detail=False)
    def alterar_ordem(request):
        cardapio = request.POST.get('id_cardapio')
        categoria_ids = request.POST.getlist('id_categorias')

        novas_ordens = {}
        for ordem, categoria_id in enumerate(categoria_ids, start=1):
            OrdemCategoriaCardapio.objects.filter(categoria=categoria_id, cardapio=cardapio).update(ordem=ordem)
            nova_ordem = OrdemCategoriaCardapio.objects.get(categoria=categoria_id, cardapio=cardapio).ordem
            novas_ordens[categoria_id] = nova_ordem

        return JsonResponse(novas_ordens)