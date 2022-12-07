from django.views.generic import CreateView
from pedidos.models.complemento import Complementos
from django.urls import reverse_lazy


class ComplementoCreate(CreateView):
    model = Complementos
    fields = '__all__'
    def get_success_url(self):
       return reverse_lazy("list_complemento")