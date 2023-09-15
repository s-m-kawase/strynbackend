from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from ...models.ordem_categoria_cardapio import OrdemCategoriaCardapio
from ..serializers.ordem_categoria_serializers import OrdemCategoriaCardapioSerializer
import django_filters.rest_framework



class OrdemCategoriaCardapioViewSet(viewsets.ModelViewSet):
    queryset = OrdemCategoriaCardapio.objects.all()
    serializer_class = OrdemCategoriaCardapioSerializer
    # permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['cardapio']

    search_fields = []

    

    @action(methods=['post'], detail=False)
    def alterar_ordem(self, request):
        cardapio_id = request.data['id_cardapio']
        categoria_ids = request.data['ids_categorias']

        for ordem, categoria_id in enumerate(categoria_ids):
            OrdemCategoriaCardapio.objects.filter(cardapio=cardapio_id, categoria=categoria_id).update(ordem=ordem)

        return Response({'status': 'success'})
    

   
    