from rest_framework import generics, serializers, viewsets
from pedidos.models import GrupoComplementos
from ..serializers.grupo_complemento_item_serializer import *


class GrupoComplementosViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = GrupoComplementos.objects.all()
    serializer_class = GrupoComplementosSerializer