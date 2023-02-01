from rest_framework import generics, serializers, viewsets
from pagamentos.models import Cupom
from ..serializers.cupom_serializers import *
from rest_framework.permissions import IsAuthenticated


class CupomViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Cupom.objects.all()
    serializer_class = CupomSerializer
