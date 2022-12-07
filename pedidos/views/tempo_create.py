from django.views.generic import CreateView
from pedidos.models.tempo import TempoEstimado
from django.urls import reverse_lazy


class TempoEstimadoCreate(CreateView):
    model = TempoEstimado
    fields = '__all__'
    def get_success_url(self):
       return reverse_lazy("list_tempo")