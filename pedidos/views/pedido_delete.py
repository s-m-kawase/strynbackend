from django.shortcuts import redirect
from pedidos.models.pedido import Pedidos


def pedido_delete(request,pk):
    iten = Pedidos.objects.get(id=pk)
    iten.delete()
    return redirect('list_pedido')