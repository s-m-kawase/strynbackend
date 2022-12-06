from django.urls import reverse_lazy
from django.views.generic import UpdateView
from pedidos.models.clientes import Cliente


class ClienteUpdate(UpdateView):
    model = Cliente
    fields = ['nome_cliente', 'cpf','celular','historico_pedido']
    


    def get_success_url(self):
       return reverse_lazy("list_cliente")

    