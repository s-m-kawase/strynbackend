from django.urls import reverse_lazy
from django.views.generic import UpdateView
from pagamentos.models.pagamento import Pagamento


class PagamentoUpdate(UpdateView):
    model = Pagamento
    fields = '__all__'

    def get_success_url(self):
       return reverse_lazy("list_pagamento")
