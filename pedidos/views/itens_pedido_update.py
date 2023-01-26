from django.urls import reverse_lazy
from django.views.generic import UpdateView
from pedidos.models.itens_pedido import ItensPedido


class ItensPedidoUpdate(UpdateView):
    model = ItensPedido
    fields = '__all__'

    def get_success_url(self):
       return reverse_lazy("list_iten_pedido")
