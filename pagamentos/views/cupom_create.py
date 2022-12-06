from django.views.generic import CreateView
from pagamentos.models.cupom import Cupom
from django.urls import reverse_lazy


class CupomCreate(CreateView):
    model = Cupom
    fields = '__all__'
    def get_success_url(self):
       return reverse_lazy("list_cupom")