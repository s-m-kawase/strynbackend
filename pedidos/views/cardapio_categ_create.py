from django.views.generic import CreateView
from pedidos.models.categoria_cardapio import CategoriaCardapio
from django.urls import reverse_lazy


class CardapioCategoriaCreate(CreateView):
    model = CategoriaCardapio
    fields = ['nome', 'status']
    def get_success_url(self):
       return reverse_lazy("list_categoria")