from django.shortcuts import redirect
from pedidos.models.itens_pedido_complementos import ItensPedidoComplementos


def itens_complemento_delete(request,pk):
    iten = ItensPedidoComplementos.objects.get(id=pk)
    iten.delete()
    return redirect('list_iten_complemento')