from django.db import connection
from rest_framework import viewsets ,filters
import django_filters.rest_framework
from pedidos.models import Pedidos,Restaurante
from pagamentos.models import Pagamento
from django.db.models import Q
from ..serializers.pedido_serializer import *
from rest_framework.decorators import action
from django.http.response import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import stripe
from decouple import config
from rest_framework.response import Response
import requests
from datetime import timedelta
from ...models import Cliente

stripe_secret_key = config('STRIPE_SECRET_KEY')
stripe.api_key = stripe_secret_key
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

def criar_cupom(pedido):
    stripe_secret_key = config('STRIPE_SECRET_KEY')
    stripe.api_key = stripe_secret_key
    if pedido.cupom and pedido.cupom.porcentagem:
        valor = pedido.cupom.porcentagem
        if pedido.cupom.valor_fixo == True:
            valor_centavos = int(valor * 100)
            cupom = stripe.Coupon.create(
            amount_off=valor_centavos,
            currency='brl', 
            duration='once',
)
        else:
            percent_off = pedido.cupom.porcentagem
            cupom = stripe.Coupon.create(
                percent_off=percent_off,
                duration="once",
            )
        return cupom
    else:
        return None


class PedidosViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = ()
    queryset = Pedidos.objects.all().order_by('-data_criacao','status_pedido','cupom')
    serializer_class = PedidosSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = []

    search_fields = ['id']


    def get_queryset(self):
        query = super().get_queryset().order_by('id')
        restaurante = self.request.query_params.get('restaurante',None)
        cliente = self.request.query_params.get('cliente',None)
        tela_cli = self.request.query_params.get('tela_cli',None)
        gestor = self.request.query_params.get('gestor',None)
        hash_pedido = self.request.query_params.get('hash_pedido',None)
        # hash_cliente = self.request.query_params.get('hash_cliente',None)
        status = self.request.query_params.get('status_pedido',None)
        data_inicial =  self.request.query_params.get('data_inicial',None)
        data_final = self.request.query_params.get('data_final', None)
        cozinha = self.request.query_params.get('cozinha', None)
        usuario = self.request.user
        if cozinha:
            query = query.order_by('hora_status_aguardando_preparo')
        if tela_cli:
            query = query.order_by('id')
        if gestor:
            query = query.order_by('status_pedido', '-id')
        if data_inicial and data_final and data_final >= data_inicial:
            query = query.filter(
                data_criacao__lte=data_final,
                data_criacao__gte=data_inicial
            )

        if usuario.is_authenticated:
            # cli = Cliente.objects.get(id=cliente)
            # eita = cli.hash_cliente
            if not usuario.is_superuser:
                hash_pedido = usuario.cliente.hash_cliente if hasattr(usuario, 'cliente') else False
                if hash_pedido:
                    query = query.filter(Q(hash_cliente=hash_pedido)|
                                        Q(cliente__usuario=usuario) |
                                        Q(restaurante__usuario=usuario)).distinct()
                else:
                    query = query.filter(Q(cliente__usuario=usuario) |
                                Q(restaurante__usuario=usuario)).distinct()
                    
        else:  
            if hash_pedido:
                query = query.filter(status_pedido__in=['Em preparo','Aguardando Preparo','Pago','Aguardando Confirmação','Aguardando Pagamento Mesa','Concluído','Cancelado','Sacola','Estornado'],
                hash_cliente=hash_pedido
                )
            elif restaurante:
              query = query.filter(restaurante=restaurante)
            else:
                query = query.none()
                
        if restaurante:
              query = query.filter(restaurante=restaurante)

        if status:
            query = query.filter(status_pedido=status)

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
        taxa_atendimento = 0
        if pedido.taxa_de_atendimento:
            taxa_atendimento = float(pedido.taxa_de_atendimento) if pedido.taxa_de_atendimento else 0
        

        # taxa_atendimento = float(subtotal) * (float(pedido.restaurante.taxa_servico) / 100.0)


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

        success_url = f'{pedido.restaurante.link_restaurante}/pedidos/?tab=andamento&status_pedido=Pago&id={pedido.id}'
        cancel_url = f'{pedido.restaurante.link_restaurante}/pedidos/?tab=andamento&status_pedido=Cancelado&id={pedido.id}'

        
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
        },
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
      # if pedido.status_pedido == 'Estornado':
      #     return Response({'mensagem': 'Pedido já foi reembolsado'}, status=200)

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
                    taxa = 0
                    if pedido and pedido.taxa_de_atendimento:
                        taxa = float(subtotal) * (float(pedido.restaurante.taxa_servico) / 100.0)
                    # taxa = float(subtotal) * (float(pedido.restaurante.taxa_servico) / 100.0)
                    

                    total_com_taxa = float(subtotal) + float(taxa)

                    # Aplica o desconto ao valor total
                    if pedido.cupom and pedido.cupom.porcentagem:
                        porcentagem_desconto = pedido.cupom.calcular_porcentagem_desconto()
                        desconto = total_com_taxa * porcentagem_desconto
                        total_reembolso = total_com_taxa - desconto
                    else:
                        total_reembolso = total_com_taxa

                    # Converte o valor do reembolso para centavos
                    amount = int(total_reembolso * 100)
                    """ amount = int(pedido.valor_pago*100) """

                    # Cria o reembolso com base no ID do 
                    refund = stripe.Refund.create(
                        payment_intent=payment_intent_id,
                        amount=amount,
                    )

                    # Atualiza o status do pedido
                    pedido.status_pedido = 'Cancelado'
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
        pedido.status_pedido = 'Cancelado'
        pedido.save()
        return Response({'mensagem': 'Reembolso realizado com sucesso'}, status=200)

    @action(detail=False, methods=['post'])
    def limpar_pedido(self, request):
        pk = request.data.get('pk',None)
        pedido = Pedidos.objects.get(id=pk)

        try:
            pedido.itenspedido_set.all().delete()
            return Response({'message': 'Itens do pedido limpos com sucesso.'}, status=200)
        except Exception as e:
            return Response({'error': 'Ocorreu um erro ao limpar os itens do pedido.'}, status=404)

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

   
# -------------------------- pix no asaas --------------------------------------
    @action(methods=['get'], detail=True)
    def criar_cobranca_asaas(self ,request,pk):
        try:
            pedido = Pedidos.objects.get(id=pk)
            
            # pegar cpf do cliente se ele tiver cadastrado
            # if pedido and pedido.cliente:
            #     pedido.cpf = pedido.cliente.cpf
            # else:
            #     pedido.cpf = None
            

            api_key = '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNjYxODE6OiRhYWNoX2MyYjBjNzVhLTFmOWQtNDljMS04YTYyLTU5OTY2ZGY3OWVkOQ=='

            data_vencimento = pedido.data_criacao + timedelta(days=1)
            data_vencimento = f"{data_vencimento}"

            valor_total = float(pedido.total)
            porcentagem = float(pedido.restaurante.pocentagem_para_tranferencia)
            porcentagem = porcentagem / 100
            valor_fixo = valor_total * porcentagem

                # "walletId": "095ca411-db88-491f-9bbd-a997e14a21eb",
            split_data = [
            {
                "walletId": pedido.restaurante.chave_asaas,
                "fixedValue": valor_fixo
            }
            ]
            
            success_url = f'{pedido.restaurante.link_restaurante}/pedidos/?tab=andamento&status_pedido=Pago&id={pedido.id}'

            if pedido.cliente:
                cpf = pedido.cliente.cpf
            else:
                cpf = pedido.cpf
            
            if pedido.cliente:
                nome = pedido.cliente.nome_cliente
            else:
                nome = pedido.nome_cliente
            # Crie uma cobrança no Asaas (sandbox)
            cobranca_data = {
                'customer': {
                    'name':  nome,
                    'cpfCnpj': cpf  
                },
                'billingType': 'PIX',
                'dueDate': data_vencimento,
                'value': pedido.total,  
                'description': f'Cobrança do pedido {pedido.id}, feito pelo {nome}',
                'externalReference': pedido.id,
                'paymentType': 'PIX',
                'split': split_data,
                "callback":{
                    "successUrl": success_url,
                    "autoRedirect": False  
                }
            }

            headers = {
                'access_token': api_key,
            }

            response = requests.post('https://sandbox.asaas.com/api/v3/payments', json=cobranca_data, headers=headers)

            if response.status_code == 200:
                cobranca = response.json()
                print("Cobrança criada com sucesso!")
                print("URL do PIX: ", cobranca['invoiceUrl'])
                return JsonResponse({
                    "checkout_url": cobranca['invoiceUrl'],
                    "url_redirecionamento":success_url
                })
            
            else:
                error_data = response.json()
                return JsonResponse({ "error": error_data})
        except Pedidos.DoesNotExist:
            return JsonResponse({"error": "Pedido não encontrado"})
        
        except requests.exceptions.RequestException as e:
            error_message = str(e)
        print("Erro durante a solicitação à API:", error_message)
        return JsonResponse({
            "error": "Erro interno do servidor",
            "error_message": error_message
        })
    
    @action(methods=['get'], detail=True)
    def reembolso_asaas(self ,request,pk):
        pedido = Pedidos.objects.get(pk=pk)
        id_do_pagamento = pedido.pagamento_asaas
        url_api_asaas = f"https://sandbox.asaas.com/api/v3/payments/{id_do_pagamento}/refund"
        headers = {
            'Content-Type': 'application/json',
            'access_token': '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNjYxODE6OiRhYWNoX2MyYjBjNzVhLTFmOWQtNDljMS04YTYyLTU5OTY2ZGY3OWVkOQ==',
        }

        dados_reembolso = {
            'value': pedido.total,  
            'description': 'Reembolso do pedido', 
        }


        try:
            resposta = requests.post(url_api_asaas, json=dados_reembolso, headers=headers)
            if resposta.status_code // 100 == 2:
                return Response({"message": "Reembolso realizado com sucesso"})
            else:
                return Response({"error": f"Falha ao realizar reembolso: {resposta.status_code} - {resposta.text}"})
        except Exception as e:
            return Response({"error": f"Erro durante a solicitação de reembolso: {str(e)}"})


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

    @action(methods=['get'], detail=False)
    def select_data(self,request):
        sql_query = f"""  SELECT DISTINCT to_char( data_criacao::date, 'FMMonthYYYY')
                          FROM pedidos_pedidos
                              """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

        keys = [column[0] for column in cursor.description]
        result_dict = [dict(zip(keys, row)) for row in result]
        return JsonResponse(result_dict, safe=False)
