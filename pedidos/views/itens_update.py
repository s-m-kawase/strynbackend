from django.urls import reverse_lazy
from django.views.generic import UpdateView
from pedidos.models.iten import Item


class ItensUpdate(UpdateView):
    model = Item
    fields = '__all__'

    def get_success_url(self):
       return reverse_lazy("list_itens")
