from django.views.generic import CreateView
from pedidos.models.restaurante import Restaurante
from django.urls import reverse_lazy


class RestauranteCreate(CreateView):
    model = Restaurante
    fields = '__all__'
    def get_success_url(self):
       return reverse_lazy("list_restaurante")