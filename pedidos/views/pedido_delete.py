from django.shortcuts import redirect
from pedidos.models.pedido import Pedido


def pedido_delete(request,pk):
    iten = Pedido.objects.get(id=pk)
    iten.delete()
    return redirect('list_pedido')