from django.shortcuts import redirect
from pedidos.models.restaurante import Restaurante


def restaurante_delete(request,pk):
    iten = Restaurante.objects.get(id=pk)
    iten.delete()
    return redirect('list_restaurante')