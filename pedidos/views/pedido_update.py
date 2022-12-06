from django.urls import reverse_lazy
from django.views.generic import UpdateView
from pedidos.models.pedido import Pedido


class PedidoUpdate(UpdateView):
    model = Pedido
    fields = '__all__'

    def get_success_url(self):
       return reverse_lazy("list_pedido")
