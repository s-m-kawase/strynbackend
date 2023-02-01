from rest_framework import generics, serializers, viewsets
from pedidos.models import GrupoComplementos
from ..serializers.grupo_complemento_item_serializer import *
from rest_framework.permissions import IsAuthenticated



class GrupoComplementosViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = GrupoComplementos.objects.all()
    serializer_class = GrupoComplementosSerializer