from rest_framework import generics, serializers, viewsets
from pedidos.models import TempoEstimado
from ..serializers.tempo_estimado_serializer import *


class TempoEstimadoViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = TempoEstimado.objects.all()
    serializer_class = TempoEstimadoSerializer