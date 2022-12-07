from django.views.generic import ListView
from pedidos.models.itens_pedido import IntensPedido


class ItensPedidoList(ListView):
    model = IntensPedido
    fileds = '__all__'

