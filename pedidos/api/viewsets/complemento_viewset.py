from rest_framework import generics, serializers, viewsets
from pedidos.models import Complementos
from ..serializers.complemento_serializer import *
from rest_framework.permissions import IsAuthenticated



class ComplementosViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Complementos.objects.all()
    serializer_class = ComplementosSerializer