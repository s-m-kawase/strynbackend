from django.shortcuts import redirect
from pedidos.models.itens_pedido import ItensPedido


def itens_pedido_delete(request,pk):
    iten = ItensPedido.objects.get(id=pk)
    iten.delete()
    return redirect('list_iten_pedido')