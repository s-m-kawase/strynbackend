from rest_framework import generics, serializers, viewsets
from pagamentos.models import Cupom
from ..serializers.cupom_serializers import *

class CupomViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Cupom.objects.all()
    serializer_class = CupomSerializer
