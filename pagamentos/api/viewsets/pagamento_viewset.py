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
    permission_classes = ()
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

        hash_cliente = self.request.query_params.get('hash',None)
        usuario = self.request.user
        if usuario.is_authenticated:
          query = query.filter(Q(pedido__cliente__usuario=usuario) |
                              Q(pedido__restaurante__usuario=usuario)).distinct()
        else:
            query = query.filter(

                Q(pedido__numero_mesa=hash_cliente,
                  pagamento='Pagamento na mesa',
                  pedido__status_pedido__in=['Em preparo','Aguardando Preparo','Pago','Aguardando Pagamento Mesa','Concluído','Cancelado','Sacola','Estornado'])|
                Q(pedido__numero_mesa=hash_cliente,
                  pagamento='Pagamento online',
                  pedido__status_pedido__in=['Em preparo','Aguardando Preparo','Pago','Concluído','Cancelado','Sacola','Estornado']))

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
        sql_query = f"""SELECT
                            CASE
                                WHEN COUNT(valor_pago) = 0 THEN 0
                                ELSE ROUND(SUM(valor_pago) / COUNT(valor_pago), 2)
                            END AS ticket_medio
                        FROM pagamentos_pagamento
                        WHERE pedido_id in (
                            SELECT id FROM pedidos_pedidos
                            WHERE data_criacao::date = CURRENT_DATE::date
                                AND restaurante_id = {restaurante_id.id});
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
        sql_query = f""" SELECT
                            CASE
                                WHEN COUNT(valor_pago) = 0 THEN 0
                                ELSE ROUND(SUM(valor_pago) / COUNT(valor_pago), 2)
                            END AS ticket_medio
                        FROM pagamentos_pagamento
                        WHERE pedido_id in (
                            SELECT id from pedidos_pedidos
                            WHERE EXTRACT(MONTH FROM data_criacao::date) = EXTRACT(MONTH FROM CURRENT_DATE::date)
                                AND restaurante_id = {restaurante_id.id});
                          """



        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

        keys = [column[0] for column in cursor.description]
        result_dict = [dict(zip(keys, row)) for row in result]
        return JsonResponse(result_dict, safe=False)

    @action(methods=['post'], detail=False)
    def financeiro_total_de_venda(self,request):
        mesano = request.data.get('mesano',None)

        sql_query = f"""SELECT
                            SUM( ROUND( pag.valor_pago - (pag.valor_pago * (COALESCE(cup.porcentagem, 0)/100)) , 2) ) AS "total_de_vendas"
                        FROM pagamentos_pagamento pag
                        LEFT JOIN pedidos_pedidos ped
                        ON pag.pedido_id = ped.id
                        LEFT JOIN pagamentos_cupom cup
                        ON ped.cupom_id = cup.id
                        WHERE to_char(ped.data_criacao::date, 'YYYY/MM') = to_char(to_date('{mesano}', 'MonthYYYY'), 'YYYY/MM')
                    """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

        keys = [column[0] for column in cursor.description]
        result_dict = [dict(zip(keys, row)) for row in result]
        return JsonResponse(result_dict, safe=False)


    @action(methods=['post'], detail=False)
    def financeiro_tabela(self,request):
        mesano = request.data.get('mesano',None)
        # profile = Profile.objects.get(user=request.user)
        restaurante =request.user.profile.restaurante

        sql_query = f"""SELECT
                            ped.data_criacao_f AS "periodo", data_criacao2 AS "data_criacao"
                            ,ROUND( SUM( pag.valor_pago - (pag.valor_pago * (COALESCE(cup.porcentagem, 0)/100)) ) , 2) AS "recebidos_pela_operadora"
                            ,ROUND( SUM( pag.valor_pago * (COALESCE(cup.porcentagem, 0)/100) ) , 2)AS incentivo
                            ,SUM( pag.valor_pago ) AS total_repasse
                        FROM pagamentos_pagamento pag
                        LEFT JOIN (
                            SELECT
                                id
                                ,TO_CHAR(data_criacao::DATE, 'DD/MM') as data_criacao_f
                                ,TO_CHAR(data_criacao::DATE, 'DD/MM/YYYY') as data_criacao2
                                ,data_criacao
                                ,cupom_id
                            FROM pedidos_pedidos
                            ) "ped"
                        ON pag.pedido_id = ped.id
                        LEFT JOIN pagamentos_cupom cup
                        ON ped.cupom_id = cup.id
                        WHERE to_char(ped.data_criacao::DATE, 'FMMonthYYYY') = '{mesano}'
                        AND ped.restaurante = {restaurante}
                        GROUP BY ped.data_criacao_f,data_criacao2
                        ORDER BY ped.data_criacao_f DESC
                    """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

        keys = [column[0] for column in cursor.description]
        result_dict = [dict(zip(keys, row)) for row in result]
        return JsonResponse(result_dict, safe=False)

    @action(methods=['post'], detail=False)
    def financeiro_tabela_por_dia(self,request):
        data_selecionada = request.data.get('data',None)

        sql_query = f"""
                        SELECT
                            ped.data_criacao_f AS periodo
                            ,ped.id
                            ,ROUND( pag.valor_pago - (pag.valor_pago * (COALESCE(cup.porcentagem, 0)/110)) - ( taxa_de_atendimento::numeric(10, 2) ), 2)::numeric(10, 2) AS valor_dos_itens
                            ,ROUND( taxa_de_atendimento::numeric(10, 2) , 2) AS taxa_de_atendimento
                            ,ROUND( pag.valor_pago * (COALESCE(cup.porcentagem, 0)::numeric(10, 2) / 100::numeric(10, 2)) , 2) AS incentivo
                            ,pag.valor_pago AS total
                        FROM pagamentos_pagamento pag
                        LEFT JOIN (
                            SELECT
                                id
                                ,TO_CHAR(data_criacao::DATE, 'DD/MM/YYYY') AS data_criacao_f
                                ,data_criacao
                                ,cupom_id
                                ,taxa_de_atendimento
                                ,restaurante_id
                            FROM pedidos_pedidos
                        ) "ped"
                        ON pag.pedido_id = ped.id
                        LEFT JOIN pagamentos_cupom cup
                        ON ped.cupom_id = cup.id
                        WHERE TO_CHAR(ped.data_criacao::DATE, 'DD/MM/YYYY') = '{data_selecionada}'
                        ORDER BY ped.data_criacao_f DESC
                        """
# linha 248 frente da variavel ::DATE  --'2023-06-20'::date  --'{data_selecionada}'
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

        keys = [column[0] for column in cursor.description]
        result_dict = [dict(zip(keys, row)) for row in result]
        return JsonResponse(result_dict, safe=False)

    @action(methods=['post'], detail=False)
    def financeiro_quantidade_venda_mes(self,request):
        mesano = request.data.get('mesano',None)

        sql_query = f"""SELECT
                            COUNT(id) AS "numero_de_vendas"
                        FROM pedidos_pedidos
                        WHERE to_char(data_criacao::date, 'FMMonthYYYY') = '{mesano}';
                      """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

        keys = [column[0] for column in cursor.description]
        result_dict = [dict(zip(keys, row)) for row in result]
        return JsonResponse(result_dict, safe=False)

    @action(methods=['post'], detail=False)
    def financeiro_tickt_indicador(self,request):
        # usuario = request.user.id
        # restaurante_id = Restaurante.objects.get(usuario=usuario)
        restaurante_id = request.data.get('restaurante_id',None)
        mesano = request.data.get('mesano',None)
        sql_query = f"""SELECT
                            CASE
                                WHEN COUNT(valor_pago) = 0 THEN 0
                                ELSE ROUND(SUM(valor_pago) / COUNT(valor_pago), 2)
                            END AS ticket_medio
                        FROM pagamentos_pagamento
                        WHERE pedido_id in (
                                  SELECT id FROM pedidos_pedidos
                                  WHERE to_char(data_criacao::date, 'FMMonthYYYY') = '{mesano}'
                                      AND restaurante_id = '{restaurante_id}');
                      """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

        keys = [column[0] for column in cursor.description]
        result_dict = [dict(zip(keys, row)) for row in result]
        return JsonResponse(result_dict, safe=False)

