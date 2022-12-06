from django.views.generic import ListView
from pedidos.models.clientes import Cliente


class ClienteList(ListView):
    model = Cliente
    fileds = '__all__'

