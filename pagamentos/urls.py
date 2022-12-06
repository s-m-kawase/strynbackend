from django.urls import path
from pagamentos.views.adicional_list import AdicionalList
from pagamentos.views.adicional_create import AdicionalCreate
from pagamentos.views.adicional_update import AdicionalUpdate
from pagamentos.views.adicional_delete import adicional_delete

from pagamentos.views.cupom_list import CupomList
from pagamentos.views.cupom_create import CupomCreate
from pagamentos.views.cupom_update import CupomUpdate
from pagamentos.views.cupom_delete import cupom_delete


from pagamentos.views.pagamento_list import PagamentoList
from pagamentos.views.pagamento_create import PagamentoCreate
from pagamentos.views.pagamento_update import PagamentoUpdate
from pagamentos.views.pagamento_delete import pagamento_delete


urlpatterns = [
    path('adicional', AdicionalList.as_view(), name='list_adicional'),
    path('adicional_novo/', AdicionalCreate.as_view(), name='create_adicional'),
    path('adicional_editar/<int:pk>/', AdicionalUpdate.as_view(), name='update_adicional'),
    path('adicional_delete/<int:pk>/', adicional_delete, name='delete_adicional'),

    path('cupom', CupomList.as_view(), name='list_cupom'),
    path('cupom_novo/', CupomCreate.as_view(), name='create_cupom'),
    path('cupom_editar/<int:pk>/', CupomUpdate.as_view(), name='update_cupom'),
    path('cupom_delete/<int:pk>/', cupom_delete, name='delete_cupom'),

    path('', PagamentoList.as_view(), name='list_pagamento'),
    path('pagamento_novo/', PagamentoCreate.as_view(), name='create_pagamento'),
    path('pagamento_editar/<int:pk>/', PagamentoUpdate.as_view(), name='update_pagamento'),
    path('pagamento_delete/<int:pk>/', pagamento_delete, name='delete_pagamento'),


]
