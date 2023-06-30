from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from ...models import Cardapio
from ..serializers.cardapio_com_ordem_serializer import CardapioComOrdemSerializer


class CardapioComOrdemViewSet(viewsets.ModelViewSet):
    queryset = Cardapio.objects.all()
    serializer_class = CardapioComOrdemSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]

    search_fields = [

    ]


    def get_queryset(self):
        query = super().get_queryset()

        parametro = self.request.query_params
        cardapio = parametro.get('cardapio',None)
        restaurante = parametro.get('restaurante',None)
        ordem = parametro.get('ordem',None)

        # Verifica se o usuário é anônimo
        if self.request.user.is_authenticated:
            if cardapio:
                query = query.filter(cardapio=cardapio)
            else:
              usuario = self.request.user
              print(usuario)
              query = query.filter(restaurante__usuario=usuario)


        elif self.request.user.is_anonymous:
            if cardapio and restaurante:
              query = query.filter(
                  id=ordem,
                  cardapio=cardapio,
                  cardapio_restaurante=restaurante
              )


        return query