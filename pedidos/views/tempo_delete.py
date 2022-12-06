from django.shortcuts import redirect
from pedidos.models.tempo import TempoEstimado


def tempo_delete(request,pk):
    iten = TempoEstimado.objects.get(id=pk)
    iten.delete()
    return redirect('list_tempo')