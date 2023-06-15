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
from django.shortcuts import redirect
from rest_framework.response import Response
from django.contrib import messages
import stripe
import time
from decouple import config

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

        success_url = f'https://stryn.netlify.app/cliente/sucesso?tab=andamento&status_pedido=Pago&id={pedido.id}'
        # Cria o checkout session do Stripe
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url='https://stryn.netlify.app/cliente/visao-geral',
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
      if pedido.session_id:
          session_id = pedido.session_id
          payment_intent_id = pedido.payment_intent_id
          if pagamento.pagamento == 'Pagamento online':

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
      else:
          return Response({'erro': 'Dados de pagamento não encontrados'}, status=500)



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
