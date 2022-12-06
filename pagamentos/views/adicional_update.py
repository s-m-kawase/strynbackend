from django.urls import reverse_lazy
from django.views.generic import UpdateView
from pagamentos.models.adicional import Adicional


class AdicionalUpdate(UpdateView):
    model = Adicional
    fields = '__all__'

    def get_success_url(self):
       return reverse_lazy("list_adicional")
