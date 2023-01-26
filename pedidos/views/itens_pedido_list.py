from django.views.generic import ListView
from pedidos.models.itens_pedido import ItensPedido


class ItensPedidoList(ListView):
    model = ItensPedido
    fileds = '__all__'

