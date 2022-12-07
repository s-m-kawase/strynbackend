from django.urls import reverse_lazy
from django.views.generic import UpdateView
from pedidos.models.complemento import Complementos


class ComplementoUpdate(UpdateView):
    model = Complementos
    fields = '__all__'
    


    def get_success_url(self):
       return reverse_lazy("list_complemento")

    