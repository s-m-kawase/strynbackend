from django.shortcuts import redirect
from pedidos.models.item_cardapio import ItemCardapio


def itens_delete(request,pk):
    iten = ItemCardapio.objects.get(id=pk)
    iten.delete()
    return redirect('list_itens')