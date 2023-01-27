from django.views.generic import CreateView
from pedidos.models.pedido import Pedidos
from django.urls import reverse_lazy


class PedidoCreate(CreateView):
    model = Pedidos
    fields = '__all__'
    def get_success_url(self):
       return reverse_lazy("list_pedido")