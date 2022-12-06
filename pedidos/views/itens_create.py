from django.views.generic import CreateView
from pedidos.models.iten import Item
from django.urls import reverse_lazy


class ItensCreate(CreateView):
    model = Item
    fields = '__all__'
    def get_success_url(self):
       return reverse_lazy("list_itens")