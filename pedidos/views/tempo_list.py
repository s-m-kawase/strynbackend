from django.views.generic import ListView
from pedidos.models.tempo import TempoEstimado


class TempoEstimadoList(ListView):
    model = TempoEstimado
    fileds = '__all__'

