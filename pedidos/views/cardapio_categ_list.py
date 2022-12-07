from django.views.generic import ListView
from pedidos.models.categoria_cardapio import CategoriaCardapio


class CadapioCategoriaList(ListView):
    model = CategoriaCardapio
    fileds = '__all__'

