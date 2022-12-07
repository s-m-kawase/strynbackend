from rest_framework import generics, serializers, viewsets
from pagamentos.models import Adicional
from ..serializers.adicional_serializers import *



class AdicionalViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Adicional.objects.all()
    serializer_class = AdicionalSerializer