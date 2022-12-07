from django.views.generic import CreateView
from pagamentos.models.pagamento import Pagamento
from django.urls import reverse_lazy


class PagamentoCreate(CreateView):
    model = Pagamento
    fields = '__all__'
    def get_success_url(self):
       return reverse_lazy("list_pagamento")