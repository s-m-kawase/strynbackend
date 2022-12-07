from django.shortcuts import redirect
from django.views.generic import DeleteView
from pedidos.models.cardapio import Cardapio


def cardapio_delete(request,pk):
    iten = Cardapio.objects.get(id=pk)
    iten.delete()
    return redirect('list_cardapio')