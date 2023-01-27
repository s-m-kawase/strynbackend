from django.urls import reverse_lazy
from django.views.generic import UpdateView
from pedidos.models.item_cardapio import ItemCardapio


class ItensUpdate(UpdateView):
    model = ItemCardapio
    fields = '__all__'

    def get_success_url(self):
       return reverse_lazy("list_itens")
