from django.shortcuts import redirect
from pedidos.models.complemento import Complementos


def complemento_delete(request,pk):
    iten = Complementos.objects.get(id=pk)
    iten.delete()
    return redirect('list_complemento')