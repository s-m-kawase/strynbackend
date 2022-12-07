from django.shortcuts import redirect
from pagamentos.models.cupom import Cupom


def cupom_delete(request,pk):
    iten = Cupom.objects.get(id=pk)
    iten.delete()
    return redirect('list_cupom')