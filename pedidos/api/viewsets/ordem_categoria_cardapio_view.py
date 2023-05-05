from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http.response import JsonResponse
from ...models.ordem_categoria_cardapio import OrdemCategoriaCardapio
from ..serializers.ordem_categoria_serializers import OrdemCategoriaCardapioSerializer


class OrdemCategoriaCardapioViewSet(viewsets.ModelViewSet):
    queryset = OrdemCategoriaCardapio.objects.all()
    serializer_class = OrdemCategoriaCardapioSerializer
    permission_classes = []

    filter_backends = [filters.SearchFilter]

    search_fields = [
        
    ]


    @action(methods=['post'], detail=False)
    def alterar_ordem(self, request):
        cardapio = request.POST.get('id_cardapio')
        categoria_ids = request.POST.getlist('id_categorias', [])

        novas_ordens = {}
        for ordem, categoria_id in enumerate(categoria_ids):
            OrdemCategoriaCardapio.objects.filter(categoria=categoria_id, cardapio=cardapio).update(ordem=ordem)

        

        return JsonResponse(
            {
                "ordens": OrdemCategoriaCardapioSerializer(OrdemCategoriaCardapio.objects.filter(cardapio=cardapio).order_by('ordem'), many=True).data
            }, 
            content_type="application/json",
        )