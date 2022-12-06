from django.urls import reverse_lazy
from django.views.generic import UpdateView
from pedidos.models.categoria_cardapio import CategoriaCardapio


class CardapioCategoriaUpdate(UpdateView):
    model = CategoriaCardapio
    fields = ['nome', 'status']
    


    def get_success_url(self):
       return reverse_lazy("list_categoria")

    