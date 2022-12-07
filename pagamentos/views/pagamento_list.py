from django.views.generic import ListView
from pagamentos.models.pagamento import Pagamento


class PagamentoList(ListView):
    model = Pagamento
    fileds = '__all__'

