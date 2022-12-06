from django.views.generic import ListView
from pedidos.models.complemento import Complementos


class ComplementoList(ListView):
    model = Complementos
    fileds = '__all__'

