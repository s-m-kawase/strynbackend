from django.views.generic import ListView
from pedidos.models.iten import Item


class ItensList(ListView):
    model = Item
    fileds = '__all__'

