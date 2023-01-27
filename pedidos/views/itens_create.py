from django.views.generic import CreateView
from pedidos.models.item_cardapio import ItemCardapio
from django.urls import reverse_lazy


class ItensCreate(CreateView):
    model = ItemCardapio
    fields = '__all__'
    def get_success_url(self):
       return reverse_lazy("list_itens")