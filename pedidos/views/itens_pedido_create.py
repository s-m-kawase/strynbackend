from django.views.generic import CreateView
from pedidos.models.itens_pedido import IntensPedido
from django.urls import reverse_lazy


class ItensPedidoCreate(CreateView):
    model = IntensPedido
    fields = '__all__'
    def get_success_url(self):
       return reverse_lazy("list_iten_pedido")