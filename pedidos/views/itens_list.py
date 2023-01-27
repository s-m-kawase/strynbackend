from django.views.generic import ListView
from pedidos.models.item_cardapio import ItemCardapio


class ItensList(ListView):
    model = ItemCardapio
    fileds = '__all__'

