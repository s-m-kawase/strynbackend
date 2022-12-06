from django.shortcuts import redirect
from pagamentos.models.pagamento import Pagamento


def pagamento_delete(request,pk):
    iten = Pagamento.objects.get(id=pk)
    iten.delete()
    return redirect('list_pagamento')