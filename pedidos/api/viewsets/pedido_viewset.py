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
    
    @action(detail=True, methods=['post'])
    def create_checkout_session(self, request, pk):
        # Pega o pedido de acordo com o id
        pedido = Pedidos.objects.get(id=pk)
        # pagamento  = Pagamento.objects.get(pedido=pedido)

        # itens_pedido = ItensPedido.objects.filter(pedido=pedido)

        # Cria uma lista de pedido criando chave no stripe
        line_items = []
        for item_pedido in pedido.itenspedido_set.all():
            # Cria um objeto com todos os item no stripe
            line_item = {
                'price_data': {
                    'currency': 'brl',
                    'unit_amount': int(item_pedido.preco) * 100,
                    'product_data': {
                        'name': item_pedido.item.nome,
                    },
                },
                'quantity': item_pedido.quantidade,
            }
            line_items.append(line_item)

        # Cria o checkout session do Stripe
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:8000/success',
            cancel_url='http://localhost:8000/cancel',
        )
        # Salva o session_id no objeto pedido
        pedido.session_id = checkout_session.id
        pedido.checkou_url = checkout_session.url
        pedido.save()

        # Redireciona para a URL do checkout do Stripe
        return redirect(checkout_session.url)

    