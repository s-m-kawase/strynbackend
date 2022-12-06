from django.shortcuts import redirect
from pedidos.models.clientes import Cliente


def cliente_delete(request,pk):
    iten = Cliente.objects.get(id=pk)
    iten.delete()
    return redirect('list_cliente')