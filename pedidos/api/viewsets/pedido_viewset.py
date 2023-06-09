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
from decouple import config

stripe_secret_key = config('STRIPE_SECRET_KEY')
stripe.api_key = stripe_secret_key
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


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

        # Calcula o valor total do pedido com a taxa de atendimento
        subtotal = 0
        for item_pedido in pedido.itenspedido_set.all():
            subtotal += item_pedido.quantidade * item_pedido.preco_item_mais_complementos
        taxa_atendimento = subtotal * (float(pedido.restaurante.taxa_serviço) / 100)
        

        # Cria uma lista de pedido criando chave no stripe
        line_items = []
        for item_pedido in pedido.itenspedido_set.all():
            # Cria um objeto para cada item do pedido
            line_item = {
                'price_data': {
                    'currency': 'brl',
                    'unit_amount': int(item_pedido.preco_item_mais_complementos) * 100,
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

        # Aplica o desconto no valor total
        cupom_desconto = pedido.cupom if pedido.cupom else None
        if cupom_desconto:
            line_item_desconto = {
                'price_data': {
                    'currency': 'brl',
                    'unit_amount': int(cupom_desconto.valor * -100),  # Valor do desconto em centavos (negativo)
                    'product_data': {
                        'name': 'Desconto',
                    },
                },
                'quantity': 1,
            }
            line_items.append(line_item_desconto)

        # Cria o checkout session do Stripe
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='https://stryn.netlify.app/cliente/sucesso',
            cancel_url='https://stryn.netlify.app/cliente/visao-geral',
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

        # Verifica se o pedido já foi reembolsado
        if pedido.status_pedido == 'Estornado':
            return Response({'mensagem': 'Pedido já foi reembolsado'}, status=200)

        # Verifica se o pedido está associado a uma sessão de pagamento
        if pedido.session_id:
            session_id = pedido.session_id
            payment_intent_id = pedido.payment_intent_id

            if payment_intent_id:
                for item_pedido in pedido.itenspedido_set.all():
                    amount = int(item_pedido.preco_item_mais_complementos * 100)
                try:
                    # Cria o reembolso com base no ID do pagamento
                    refund = stripe.Refund.create(
                        payment_intent=payment_intent_id,
                        amount = amount,
                    )

                    # Atualiza o status do pedido 
                    pedido.status_pedido = 'Estornado'
                    pedido.save()

                    return Response({'mensagem': 'Reembolso realizado com sucesso'}, status=200)
                except stripe.error.StripeError as e:
                    error_message = str(e)
                    return Response({'erro': error_message}, status=500)

        return Response({'erro': 'Dados de pagamento não encontrados'}, status=500)
