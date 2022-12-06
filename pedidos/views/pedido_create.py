from django.views.generic import CreateView
from pedidos.models.pedido import Pedido
from django.urls import reverse_lazy


class PedidoCreate(CreateView):
    model = Pedido
    fields = '__all__'
    def get_success_url(self):
       return reverse_lazy("list_pedido")