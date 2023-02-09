from rest_framework.decorators import action
from django.http.response import JsonResponse
from rest_framework import viewsets, filters
import django_filters.rest_framework
from pagamentos.models import Cupom
from ..serializers.cupom_serializers import *
from rest_framework.permissions import IsAuthenticated
from datetime import date, datetime
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CupomViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = Cupom.objects.all()
    serializer_class = CupomSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['validado_ate']

    search_fields = ['nome']


    @action(methods=['get'], detail=False)
    def cupom_valido_ate(self, request):
        cod_cupom = request.query_params.get('cod_cupom',None)
        data_atual =datetime.today()
        mensagem = ''

        try: 
            cupom = Cupom.objects.get(cod_cupom=cod_cupom)
            cupom_serializado = CupomSerializer(cupom).data
        except:
            cupom = None
            cupom_serializado = None

        if cupom and cupom.validado_ate >= data_atual:
            mensagem = 'Válido'
            
        elif cupom:
            mensagem ='Expirado'
        
        else:
            mensagem = 'Cupom não encontrado'

            
        return JsonResponse(
            {
                "mensagem":mensagem,
                "cupom":cupom_serializado
            }, 
            content_type="application/json",
        )
      

