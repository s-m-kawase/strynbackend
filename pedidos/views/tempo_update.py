from django.urls import reverse_lazy
from django.views.generic import UpdateView
from pedidos.models.tempo import TempoEstimado


class TempoEstimadoUpdate(UpdateView):
    model = TempoEstimado
    fields = '__all__'

    def get_success_url(self):
       return reverse_lazy("list_tempo")
