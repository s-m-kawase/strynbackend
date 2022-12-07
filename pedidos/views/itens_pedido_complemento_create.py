from django.views.generic import CreateView
from pedidos.models.itens_pedido_complementos import ItensPedidoComplementos
from django.urls import reverse_lazy


class ItensPedidoComplementoCreate(CreateView):
    model = ItensPedidoComplementos
    fields = '__all__'
    def get_success_url(self):
       return reverse_lazy("list_iten_complemento")