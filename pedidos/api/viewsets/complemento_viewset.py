from rest_framework import generics, serializers, viewsets
from pedidos.models import Complementos
from ..serializers.complemento_serializer import *


class ComplementosViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Complementos.objects.all()
    serializer_class = ComplementosSerializer