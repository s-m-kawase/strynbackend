from django.urls import reverse_lazy
from django.views.generic import UpdateView
from pagamentos.models.cupom import Cupom


class CupomUpdate(UpdateView):
    model = Cupom
    fields = '__all__'

    def get_success_url(self):
       return reverse_lazy("list_cupom")
