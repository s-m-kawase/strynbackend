from django.views.generic import ListView
from pedidos.models.restaurante import Restaurante


class RestauranteList(ListView):
    model = Restaurante
    fileds = '__all__'

