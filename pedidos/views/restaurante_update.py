from django.urls import reverse_lazy
from django.views.generic import UpdateView
from pedidos.models.restaurante import Restaurante


class RestauranteUpdate(UpdateView):
    model = Restaurante
    fields = '__all__'

    def get_success_url(self):
       return reverse_lazy("list_restaurante")
