from django.views.generic import CreateView
from pagamentos.models.adicional import Adicional
from django.urls import reverse_lazy


class AdicionalCreate(CreateView):
    model = Adicional
    fields = '__all__'
    def get_success_url(self):
       return reverse_lazy("list_adicional")