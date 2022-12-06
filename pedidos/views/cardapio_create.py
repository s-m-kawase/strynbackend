from django.views.generic import CreateView
from pedidos.models.cardapio import Cardapio
from django.urls import reverse_lazy


class CardapioCreate(CreateView):
    model = Cardapio
    fields = ['nome', 'itens','categorias','restaurante']
    def get_success_url(self):
       return reverse_lazy("list_cardapio")