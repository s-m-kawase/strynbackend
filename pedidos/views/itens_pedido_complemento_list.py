from django.views.generic import ListView
from pedidos.models.itens_pedido_complementos import ItensPedidoComplementos


class ItensPedidoComplementoList(ListView):
    model = ItensPedidoComplementos
    fileds = '__all__'

