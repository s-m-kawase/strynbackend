from django.views.generic import CreateView
from pedidos.models.clientes import Cliente
from django.urls import reverse_lazy


class ClienteCreate(CreateView):
    model = Cliente
    fields = ['nome_cliente', 'cpf','celular','historico_pedido']
    def get_success_url(self):
       return reverse_lazy("list_cliente")