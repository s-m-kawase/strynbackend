from django.shortcuts import redirect
from pagamentos.models.adicional import Adicional


def adicional_delete(request,pk):
    iten = Adicional.objects.get(id=pk)
    iten.delete()
    return redirect('list_adicional')