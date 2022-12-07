from django.views.generic import ListView
from pedidos.models.pedido import Pedido


class PedidoList(ListView):
    model = Pedido
    fileds = '__all__'

