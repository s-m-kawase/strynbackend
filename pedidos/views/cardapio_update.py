from django.urls import reverse_lazy
from django.views.generic import UpdateView
from pedidos.models.cardapio import Cardapio


class CardapioUpdate(UpdateView):
    model = Cardapio
    fields = ['nome', 'itens','categorias','restaurante']
    


    def get_success_url(self):
       return reverse_lazy("list_cardapio")

    