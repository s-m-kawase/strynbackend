from rest_framework import viewsets, filters
import django_filters.rest_framework
from pagamentos.models import Pagamento
from ..serializers.pagamento_serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.decorators import action
from django.http.response import JsonResponse
from django.db import connection
from pedidos.models import Restaurante


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
    ordering_fields = "__all__"

    search_fields = ['valor_pago']

    def get_queryset(self):
        query = super().get_queryset()

        usuario = self.request.user
        query = query.filter(Q(pedido__cliente__usuario=usuario) |
                             Q(pedido__restaurante__usuario=usuario))
        return query


    @action(methods=['get'], detail=False)
    def venda_do_dia(self,request):
        usuario = request.user.id
        restaurante_id = Restaurante.objects.get(usuario=usuario)
        sql_query = f""" SELECT
                            (DATE_TRUNC('hour', data_criacao)::time AT TIME ZONE 'UTC+3')::time AS intervalo,
                            COUNT(*) AS pedidos_concluidos
                        FROM
                            pedidos_pedidos
                        WHERE
                          data_criacao::date = current_date::date
                          AND status_pedido = 'Concluído' and restaurante_id = {restaurante_id.id}
                        GROUP BY
                            intervalo
                        ORDER BY
                            intervalo;
                          """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

        keys = [column[0] for column in cursor.description]
        result_dict = [dict(zip(keys, row)) for row in result]
        return JsonResponse(result_dict, safe=False)

    @action(methods=['get'], detail=False)
    def vendas_por_mes(self,request):
        usuario = request.user.id
        restaurante_id = Restaurante.objects.get(usuario=usuario)
        sql_query = f""" SELECT
                            data_criacao::date AS intervalo,
                            COUNT(*) AS contagem
                        FROM
                            pedidos_pedidos
                        WHERE
                            EXTRACT(MONTH FROM data_criacao::date) >= EXTRACT(MONTH FROM CURRENT_DATE::date)
                            AND status_pedido = 'Concluído' and restaurante_id = {restaurante_id.id}
                        GROUP BY
                            intervalo
                        ORDER BY
                            intervalo;
                          """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

        keys = [column[0] for column in cursor.description]
        result_dict = [dict(zip(keys, row)) for row in result]
        return JsonResponse(result_dict, safe=False)


    @action(methods=['get'], detail=False)
    def ticket_medio_do_dia(self,request):
        usuario = request.user.id
        restaurante_id = Restaurante.objects.get(usuario=usuario)
        sql_query = f""" select  round(coalesce(sum(valor_pago),0)/count(valor_pago),2) ticket_medio
                        from pagamentos_pagamento
                        where pedido_id in (
                        select id from pedidos_pedidos
                        WHERE
                            data_criacao::date = CURRENT_DATE::date and restaurante_id = {restaurante_id.id}
                            );
                          """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

        keys = [column[0] for column in cursor.description]
        result_dict = [dict(zip(keys, row)) for row in result]
        return JsonResponse(result_dict, safe=False)

    @action(methods=['get'], detail=False)
    def ticket_medio_do_mes(self,request):
        usuario = request.user.id
        restaurante_id = Restaurante.objects.get(usuario=usuario)
        sql_query = f""" select round(coalesce(sum(valor_pago),0)/count(valor_pago),2) ticket_medio
                        from pagamentos_pagamento
                        where pedido_id in (
                        select id from pedidos_pedidos
                        WHERE
                            EXTRACT(MONTH FROM data_criacao::date) = EXTRACT(MONTH FROM CURRENT_DATE::date) and restaurante_id = {restaurante_id.id}
                            );
                          """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

        keys = [column[0] for column in cursor.description]
        result_dict = [dict(zip(keys, row)) for row in result]
        return JsonResponse(result_dict, safe=False)


    """ @action(detail=False, methods=['GET'])
    def total_repasse(self, request):

        todos_pagamentos = Pagamento.objects.all()
      # Filtros por dia , semana ,mes e ano
        parametros = self.request.query_params
        data_atual = date.today()

        data_inicial = parametros.get('data_inicial',None)
        data_final = parametros.get('data_final',None)
        tipo_filtro = parametros.get('tipo_filtro','diario') if parametros.get('tipo_filtro','diario') else 'diario'

        try:
            data_inicial = datetime.strptime(data_inicial, '%d-%m-%Y').date()
            data_final = datetime.strptime(data_final, '%d-%m-%Y').date()

            if data_final < data_inicial:
                raise ValueError()
        except ValueError:
            return JsonResponse(
                {
                    "error": "Período inválido"
                },
                content_type="application/json",
                status=400
            )
        valor_total = 0
        total_repasse = 0
        relatorio_diario = []
        relatorio_repase = []
        data_base = data_inicial
        while data_base <= data_final:
            if tipo_filtro == 'diario':
                pagamentos = todos_pagamentos.filter(
                   pedido__data_criacao__day=data_base.day,
                   pedido__data_criacao__month=data_base.month,
                   pedido__data_criacao__year=data_base.year,
                )
            elif tipo_filtro == 'semanal':
                start_date = data_base - timedelta(days=data_base.weekday())
                end_date = start_date + timedelta(days=6)
                pagamentos = todos_pagamentos.filter(
                    pedido__data_criacao__range=(start_date, end_date)
                )
            elif tipo_filtro == 'mensal':
                pagamentos = todos_pagamentos.filter(
                    pedido__data_criacao__month=data_base.month,
                    pedido__data_criacao__year=data_base.year
                )
            elif tipo_filtro == 'anual':
                pagamentos = todos_pagamentos.filter(
                    pedido__data_criacao__year=data_base.year
                )
            repasse = 0
            valor = 0
            for pagamento in pagamentos:
                valor += pagamento.valor_pago
                valor_total += pagamento.valor_pago if pagamento.valor_pago else 0
                repasse += 1
                total_repasse += 1
                relatorio_diario.append({
                    "data": pagamento.pedido.data_criacao.strftime('%d/%m/%Y'),
                    "valor": pagamento.valor_pago,
                    "repasse": repasse
                })
            print(f"Data base: {data_base}, Pagamentos encontrados: {len(pagamentos)}")


            data = refatorar_data_por_periodo(data_base, tipo_filtro)

            relatorio_repase.append({
                "data": data,
                "valor": valor,
                "Numero_repasse": repasse,
                "repasase":[PagamentoSerializer(s).data for s in pagamentos],
            })

            if tipo_filtro == 'diario':
                data_base += timedelta(days=1)
            elif tipo_filtro == 'semanal':
                data_base += timedelta(weeks=1)
            elif tipo_filtro == 'mensal':
                data_base += relativedelta(months=1)
            elif tipo_filtro == 'anual':
                data_base += relativedelta(years=1)

        context = {
            "relatorio_diario": relatorio_diario,
            "relatorio_repase": relatorio_repase,
            "valor_total": valor_total,
            "total_repasse": total_repasse
        }

        return JsonResponse(
            context,
            content_type="application/json"
        ) """