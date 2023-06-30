from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
from ...models import Cardapio
from ..serializers.cardapio_com_ordem_serializer import CardapioComOrdemSerializer



class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user and request.user.is_superuser

class CardapioComOrdemViewSet(viewsets.ModelViewSet):
    queryset = Cardapio.objects.all()
    serializer_class = CardapioComOrdemSerializer
    permission_classes = [IsAdminOrReadOnly,]

    filter_backends = [filters.SearchFilter]

    search_fields = [

    ]


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