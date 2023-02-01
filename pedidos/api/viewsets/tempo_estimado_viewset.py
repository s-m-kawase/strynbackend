from rest_framework import generics, serializers, viewsets
from pedidos.models import TempoEstimado
from ..serializers.tempo_estimado_serializer import *
from rest_framework.permissions import IsAuthenticated



class TempoEstimadoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = TempoEstimado.objects.all()
    serializer_class = TempoEstimadoSerializer