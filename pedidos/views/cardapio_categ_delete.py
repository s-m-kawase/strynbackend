from django.shortcuts import redirect
from pedidos.models.categoria_cardapio import CategoriaCardapio


def cardapio_categoria_delete(request,pk):
    iten = CategoriaCardapio.objects.get(id=pk)
    iten.delete()
    return redirect('list_categoria')