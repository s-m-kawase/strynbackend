from django.db import connection
from rest_framework import viewsets ,filters
import django_filters.rest_framework
from pedidos.models import Pedidos,Restaurante, ItensPedido
from pagamentos.models import Pagamento
from django.db.models import Q
from ..serializers.pedido_serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http.response import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import stripe
from decouple import config
from global_functions.functions import refatorar_data_por_periodo
from django.db.models import Sum
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta

stripe_secret_key = config('STRIPE_SECRET_KEY')
stripe.api_key = stripe_secret_key
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

def criar_cupom(pedido):
    stripe_secret_key = config('STRIPE_SECRET_KEY')
    stripe.api_key = stripe_secret_key
    if pedido.cupom and pedido.cupom.valor:
        percent_off = pedido.cupom.calcular_porcentagem_desconto()
        cupom = stripe.Coupon.create(
            percent_off=percent_off,
            duration="once",
        )
        return cupom
    else:
        return None


class PedidosViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    # permission_classes = (IsAuthenticated,)
    queryset = Pedidos.objects.all().order_by('-data_criacao')
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

    @action(detail=True, methods=['get'])
    def create_checkout_session(self, request, pk):
        # Pega o pedido de acordo com o id
        pedido = Pedidos.objects.get(id=pk)

        cupom = criar_cupom(pedido)
        cupom_id = cupom.id if cupom else None

        # Calcula o valor total do pedido com a taxa de atendimento
        subtotal = 0.0
        for item_pedido in pedido.itenspedido_set.all():
            subtotal += float(item_pedido.quantidade * item_pedido.preco_item_mais_complementos)

        taxa_atendimento = float(subtotal) * (float(pedido.restaurante.taxa_servico) / 100.0)


        # Cria uma lista de pedido criando chave no stripe
        line_items = []
        for item_pedido in pedido.itenspedido_set.all():
            # Cria um objeto para cada item do pedido
            line_item = {
                'price_data': {
                    'currency': 'brl',
                    'unit_amount': int(item_pedido.preco_item_mais_complementos * 100),
                    'product_data': {
                        'name': item_pedido.item.nome,
                    },
                },
                'quantity': item_pedido.quantidade,
            }
            line_items.append(line_item)



        # Adiciona o line_item para a taxa de atendimento
        line_item_taxa_atendimento = {
            'price_data': {
                'currency': 'brl',
                'unit_amount': int(taxa_atendimento * 100),
                'product_data': {
                    'name': 'Taxa de Atendimento',
                },
            },
            'quantity': 1,
        }
        line_items.append(line_item_taxa_atendimento)

        success_url = f'https://stryn.netlify.app/cliente/pedidos/?tab=andamento&status_pedido=Pago&id={pedido.id}'
        cancel_url = f'https://stryn.netlify.app/cliente/pedidos/?tab=andamento&status_pedido=Cancelado&id={pedido.id}'
        # Cria o checkout session do Stripe
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            discounts=[{
                'coupon': cupom_id
            }] if cupom_id else [],  # Adicionar o desconto ao carrinho
            metadata={
                'pedido_id': str(pedido.id),  # Adiciona o ID do pedido como metadado
            }
        )

        # Salva o session_id no objeto pedido
        pedido.session_id = checkout_session.id
        pedido.payment_intent_id = checkout_session.payment_intent
        pedido.save()

        Pagamento.objects.create(
            pedido=pedido,
            pagamento="Pagamento online",
            valor_pago=pedido.total,
            codigo_pagamento=checkout_session.payment_intent
            )

        # Redireciona para a URL do checkout do Stripe
        return Response({'checkout_url': checkout_session.url, 'session_id': checkout_session.id})

    @action(detail=True, methods=['get'])
    def solicitar_reembolso(self, request, pk):
      pedido = Pedidos.objects.get(id=pk)
      pagamento = Pagamento.objects.get(pedido=pedido)

      # Verifica se o pedido já foi reembolsado
      if pedido.status_pedido == 'Estornado':
          return Response({'mensagem': 'Pedido já foi reembolsado'}, status=200)

      # Verifica se o pedido está associado a uma sessão de pagamento
      if pagamento.pagamento == 'Pagamento online':
        if pedido.session_id:
            session_id = pedido.session_id
            payment_intent_id = pedido.payment_intent_id

            if payment_intent_id:
                try:

                    subtotal = 0.0
                    for item_pedido in pedido.itenspedido_set.all():
                        subtotal += float(item_pedido.quantidade * item_pedido.preco_item_mais_complementos)

                    taxa = float(subtotal) * (float(pedido.restaurante.taxa_servico) / 100.0)

                    total_com_taxa = float(subtotal) + float(taxa)

                    # Aplica o desconto ao valor total
                    if pedido.cupom and pedido.cupom.valor:
                        porcentagem_desconto = pedido.cupom.calcular_porcentagem_desconto()
                        desconto = total_com_taxa * porcentagem_desconto
                        total_reembolso = total_com_taxa - desconto
                    else:
                        total_reembolso = total_com_taxa

                    # Converte o valor do reembolso para centavos
                    amount = int(total_reembolso * 100)
                    """ amount = int(pedido.valor_pago*100) """

                    # Cria o reembolso com base no ID do pagamento
                    refund = stripe.Refund.create(
                        payment_intent=payment_intent_id,
                        amount=amount,
                    )

                    # Atualiza o status do pedido
                    pedido.status_pedido = 'Estornado'
                    pedido.save()

                    return Response({'mensagem': 'Reembolso realizado com sucesso'}, status=200)
                except stripe.error.StripeError as e:
                    error_message = str(e)
                    return Response({'erro': error_message}, status=500)
            else:
                return Response({'erro': 'Dados de pagamento não encontrados'}, status=500)
        return Response({'erro': 'Dados de pagamento não encontrados'}, status=500)
      else:
        # aqui sera feito reembolso se o status for pagamento pagar na mesa
        pedido.status_pedido = 'Estornado'
        pedido.save()
        return Response({'mensagem': 'Reembolso realizado com sucesso'}, status=200)




    @action(detail=True, methods=['get'])
    def tela_pedido_confirmado(self, request, pk):
        pedido = Pedidos.objects.get(id=pk)

        # Obter os dados do pedido do Stripe usando o intent_payment_id
        intent_payment_id = pedido.payment_intent_id
        try:
            intent = stripe.PaymentIntent.retrieve(intent_payment_id)
            taxa_servico = pedido.total_taxa_servico_no_pedido
            dados_pedido = {
                'id': intent.id,
                'valor': intent.amount / 100,  # Converter para valor em reais
                'status': intent.status,
                'nome_cliente': intent.charges.data[0].billing_details.name,
                'ultimo_numero_cartao': intent.charges.data[0].payment_method_details.card.last4,
                'taxa_de_servico':taxa_servico,
                'itens': [],
            }

            # Obter os itens do pedido
            for item in pedido.itenspedido_set.all():
              item_pedido = {
                  'nome': item.item.nome,
                  'quantidade': item.multiplicador_item_pedido,
                  'valor_unidade': item.valor_unitario_item,
                  'valor_total_item':item.preco_item_mais_complementos,
              }
              dados_pedido['itens'].append(item_pedido)


            return Response(dados_pedido)

        except stripe.error.StripeError as e:
            mensagem_erro = str(e)  # Obtém a mensagem de erro da exceção
            return Response({'error': mensagem_erro}, status=500)

    @action(detail=True, methods=['get'])
    def criar_pagamento_na_mesa(self,request,pk):
      pedido = Pedidos.objects.get(id=pk)

      Pagamento.objects.create(
          pedido=pedido,
          pagamento="Pagamento na mesa",
          valor_pago=pedido.total,
          codigo_pagamento=f"PM{pedido.id}"
      )

      return JsonResponse({"message":'success'})


#--------------------------- relatorio para grafico------------------------------


    @action(methods=['get'], detail=False)
    def pedidos_por_horario(self,request):
        usuario = request.user.id
        restaurante_id = Restaurante.objects.get(usuario=usuario)
        sql_query = f""" SELECT
                            (DATE_TRUNC('hour', data_criacao)::time AT TIME ZONE 'UTC+3')::time AS intervalo,
                            COUNT(*) AS pedidos_concluidos
                        FROM
                            pedidos_pedidos
                        WHERE
                          data_criacao::date = current_date::date and restaurante_id = {restaurante_id.id}
                        GROUP BY
                            intervalo
                        ORDER BY
                            intervalo;  """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

        keys = [column[0] for column in cursor.description]
        result_dict = [dict(zip(keys, row)) for row in result]
        return JsonResponse(result_dict, safe=False)

    @action(methods=['get'], detail=False)
    def periodos_por_dia(self,request):
        usuario = request.user.id
        restaurante_id = Restaurante.objects.get(usuario=usuario)
        sql_query = f""" SELECT
                            data_criacao::date AS intervalo,
                            COUNT(*) AS contagem
                        FROM
                            pedidos_pedidos
                        WHERE
                            data_criacao::date >= CURRENT_DATE - INTERVAL '7 days' and restaurante_id = {restaurante_id.id}
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
    def pedidos_do_dia(self,request):
        usuario = request.user.id
        restaurante_id = Restaurante.objects.get(usuario=usuario)

        sql_query = f""" select count(valor_pago) as pedidos_hoje,  coalesce(sum(valor_pago),0) as valor_hoje
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
    def pedido_do_mes(self,request):
        usuario = request.user.id
        restaurante_id = Restaurante.objects.get(usuario=usuario)
        sql_query = f"""   select count(valor_pago) as pedidos_hoje,  coalesce(sum(valor_pago),0) as valor_hoje
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


    """ @action(detail=False, methods=['get'])
    def relatorio_por_periodo(self,request):
        parametros = self.request.query_params

        todos_pedidos = Pedidos.objects.all()

        # manipulação do periodo
        data_atual = date.today()

        data_inicial = parametros.get('data_inicial', False)
        data_final = parametros.get('data_final', False)
        tipo_filtro = parametros.get('tipo_filtro', 'diario') if parametros.get('tipo_filtro', 'diario') else 'diario'


        if not data_inicial and not data_final:

            ### Tipo de periodo por dia/mes/ano
            if tipo_filtro=='diario':
                data_inicial = data_atual - relativedelta(days=10)
            elif tipo_filtro=='mensal':
                data_inicial = data_atual - relativedelta(months=12)
            elif tipo_filtro=='anual':
                data_inicial = data_atual - relativedelta(years=2)
            else:
                return JsonResponse(
                    {
                        "error": "Tipo de filtro inválido"
                    },
                    content_type="application/json",
                    status=400
                )

            data_final = data_atual

        else:
            try:
                data_inicial = datetime.strptime(data_inicial, '%d-%m-%Y').date()
                data_final = datetime.strptime(data_final, '%d-%m-%Y').date()

                if data_final < data_inicial:
                    raise ValueError()
            except:
                return JsonResponse(
                    {
                        "error": "Periodo inválido"
                    },
                    content_type="application/json",
                    status=400
                )

        # gerando o objeto para o relatório de contas a receber
        valor_total = 0
        total_venda = 0
        relatorio_pedidos = []
        data_base = data_inicial
        while(data_base <= data_final):
            if tipo_filtro == 'diario':
                pedidos = todos_pedidos.filter(
                    data_criacao__day=data_base.day,
                    data_criacao__month=data_base.month,
                    data_criacao__year=data_base.year,
                )
            elif tipo_filtro == 'mensal':
                pedidos = todos_pedidos.filter(
                    data_criacao__month=data_base.month,
                    data_criacao__year=data_base.year,
                )
            elif tipo_filtro == 'anual':
                pedidos = todos_pedidos.filter(
                    data_criacao__year=data_base.year,
                )

            venda = 0
            valor = 0
            for pedido in pedidos:
                valor += pedido.total if pedido.total else 0
                valor_total += pedido.total if pedido.total else 0
                venda +=1
                total_venda += 1

            data = refatorar_data_por_periodo(data_base, tipo_filtro)

            relatorio_pedidos.append({
                "data": data,
                "valor":valor,
                "numero_de_vendas":venda,


            })

            if tipo_filtro=='diario':
                data_base+=relativedelta(days=1)
            elif tipo_filtro=='mensal':
                data_base+= relativedelta(months=1)
            elif tipo_filtro=='anual':
                data_base+= relativedelta(years=1)


        context = {
            "relatorio_pedidos": relatorio_pedidos,
            "valor_total": valor_total,
            "total_vendas":total_venda,
        }

        return JsonResponse(
            context,
            content_type="application/json"
        )


    @action(detail=False, methods=['get'])
    def relatorio_por_hora(self, request):
        data_atual = datetime.now()
        data_inicial = data_atual - timedelta(hours=24)
        data_final = data_atual

        hora_inicial = data_inicial.replace(minute=0, second=0, microsecond=0)
        hora_final = data_final.replace(minute=59, second=59, microsecond=999)

        relatorio_por_horario = []
        total_venda = 0
        total_valor = 0
        if hora_inicial <= hora_final:
            hora_arredondada = hora_inicial
            while hora_arredondada <= hora_final:
                pedidos = Pedidos.objects.filter(
                    data_criacao__range=(hora_arredondada, hora_arredondada.replace(minute=59, second=59, microsecond=999))
                )
                venda = 0
                valor = 0
                for pedido in pedidos:
                    valor +=pedido.total if pedido.total else 0
                    total_valor += pedido.total if pedido.total else 0
                    venda +=1
                    total_venda += 1

                data_base = hora_arredondada
                tipo_filtro = 'horario'
                data = refatorar_data_por_periodo(data_base, tipo_filtro)

                relatorio_por_horario.append({
                    "data": data,
                    "valor": valor,
                    "numero_de_venda":venda,
                })


                hora_arredondada += timedelta(hours=1)
        else:
            pedidos = Pedidos.objects.none()


        context = {
            "relatorio_por_horario": relatorio_por_horario,
            "valor_total": total_valor,
            "total_vendas":total_venda,
        }

        return JsonResponse(
            context,
            content_type="application/json"
        ) """
