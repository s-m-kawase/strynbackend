from rest_framework import viewsets ,filters
import django_filters.rest_framework
from pedidos.models import Pedidos,Restaurante
from django.db.models import Q
from ..serializers.pedido_serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http.response import JsonResponse
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PedidosViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = Pedidos.objects.all()
    serializer_class = PedidosSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['status_pedido','restaurante']

    search_fields = ['id']


    def get_queryset(self):
        query = super().get_queryset()

        usuario = self.request.user
        query = query.filter(Q(cliente__usuario=usuario) |
                             Q(restaurante__usuario=usuario))

        restaurante = self.request.query_params.get('restaurante',None)
        status = self.request.query_params.get('status_pedido',None)
        data_inicial =  self.request.query_params.get('data_inicial',None)
        data_final = self.request.query_params.get('data_final', None)

        if data_inicial and data_final and data_final >= data_inicial:
            query = query.filter(
                data_criacao__lte=data_final,
                data_criacao__gte=data_inicial
            )

        if restaurante:
            query = query.filter(restaurante=restaurante)

        if status:
            query = query.filter(status_pedido=status)
        
        if usuario:
            query = query.filter(restaurante__usuario=usuario)
    
        return query


    