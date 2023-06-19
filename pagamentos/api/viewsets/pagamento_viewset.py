from rest_framework import viewsets, filters
import django_filters.rest_framework
from pagamentos.models import Pagamento
from ..serializers.pagamento_serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.http.response import JsonResponse
from global_functions.functions import refatorar_data_por_periodo

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PagamentoViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = {
            "pedido__data_criacao" :[
                "exact" ,
                "lt" ,
                "lte" ,
                "gt" ,
                "gte" ,
            ]
        }

    search_fields = ['valor_pago']

    def get_queryset(self):
        query = super().get_queryset()

        usuario = self.request.user
        query = query.filter(Q(pedido__cliente__usuario=usuario) |
                             Q(pedido__restaurante__usuario=usuario))

        # Filtros por dia , semana ,mes e ano
        parametros = self.request.query_params
        data_atual = date.today()

        data_inicial = parametros.get('data_inicio',None)
        data_final = parametros.get('data_fim',None)
        tipo_filtro = parametros.get('tipo_filtro','diario') if parametros.get('tipo_filtro','diario') else 'diario'

        if not data_inicial and not data_final:
            ### Tipo de periodo por dia/semana/mes/ano
            if tipo_filtro == 'diario' :
                data_inicial = data_atual - relativedelta(days=10)
            elif tipo_filtro == 'semanal' :
                data_inicial = data_atual - relativedelta(weeks=1)
            elif tipo_filtro == 'mensal' :
                data_inicial = data_atual - relativedelta(months=12)
            elif tipo_filtro == 'anual' :
                data_inicial = data_atual - relativedelta(years=2)

            data_final = data_atual

        else :
            try :
                data_inicial = datetime.strftime(data_inicial, '%d-%m-%Y')
                data_final = datetime.strftime(data_final, '%d-%m-%Y')

                if data_final < data_inicial :
                    raise ValueError()
            except :
                return JsonResponse(
                    {
                        "error" : "Periodo inválido"
                    },
                    content_type = "application/json",
                    status=400
                  )
            return query
            """ data_base = data_inicial
            while (data_base < data_final):
                if tipo_filtro == 'diario':
                    pagamentos = pagamento.filter(
                        pedido__data_criacao=data_base
                    )
                elif tipo_filtro == 'semanal':
                  start_date = data_base - timedelta(days=data_base.weekday())
                  end_date = start_date + timedelta(days=6)
                  pagamentos = pagamento.filter(
                      pedido__data_criacao__range=(start_date, end_date))
                elif tipo_filtro == 'mensal':
                    pagamentos = pagamento.filter(
                        pedido__data_criacao__month=data_base.month,
                        pedido__data_criacao__year=data_base.year,
                    )
                elif tipo_filtro == 'anual':
                    pagamentos = pagamento.filter(
                        pedido__data_criacao__year=data_base.year,
                    )
               data = refatorar_data_por_periodo(data_base, tipo_filtro)

                if tipo_filtro == 'diario':
                    data_base += timedelta(days=1)
                elif tipo_filtro == 'semanal':
                    data_base += timedelta(weeks=1)
                elif tipo_filtro == 'mensal':
                    data_base += relativedelta(months=1)
                elif tipo_filtro == 'anual':
                    data_base += relativedelta(years=1) """


