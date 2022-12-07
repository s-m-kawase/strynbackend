from django.shortcuts import redirect
from pedidos.models.grupo_complemento import GrupoComplementos


def grupo_complemento_delete(request,pk):
    iten = GrupoComplementos.objects.get(id=pk)
    iten.delete()
    return redirect('list_grupo_complemento')