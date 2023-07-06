from rest_framework import viewsets, filters
import django_filters.rest_framework
from pedidos.models import Cliente
from ..serializers.cliente_serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.http.response import JsonResponse

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ClienteViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = ()
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = []

    search_fields = ['nome_cliente']


    @action(methods=['get'], detail=False)
    def usuario_logado(self, request):

      user = request.user
      cliente = Cliente.objects.get(usuario=user)
      context = ({
          "id":cliente.id,
          "username":cliente.user.username,
          "first_name":cliente.user.first_name,
          "last_name":cliente.user.last_name,
          "email":cliente.user.email,
          "is_staff":cliente.user.is_staff,
          "is_superuser":cliente.user.is_superuser
      })


      return JsonResponse(context, content_type="application/json", safe=False)