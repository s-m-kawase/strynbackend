from rest_framework import generics, serializers, viewsets
from pagamentos.models import Adicional
from ..serializers.adicional_serializers import *

from rest_framework.permissions import IsAuthenticated



class AdicionalViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Adicional.objects.all()
    serializer_class = AdicionalSerializer