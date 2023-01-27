from django.views.generic import ListView
from pedidos.models.pedido import Pedidos


class PedidoList(ListView):
    model = Pedidos
    fileds = '__all__'

