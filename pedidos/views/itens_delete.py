from django.shortcuts import redirect
from pedidos.models.iten import Item


def itens_delete(request,pk):
    iten = Item.objects.get(id=pk)
    iten.delete()
    return redirect('list_itens')