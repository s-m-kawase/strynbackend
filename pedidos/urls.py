from django.urls import path
from pedidos.views.cardapio_list import CadapioList
from pedidos.views.cardapio_create import CardapioCreate
from pedidos.views.cardapio_update import CardapioUpdate
from pedidos.views.cardapio_delete import cardapio_delete

from pedidos.views.cardapio_categ_list import CadapioCategoriaList
from pedidos.views.cardapio_categ_create import CardapioCategoriaCreate
from pedidos.views.cardapio_categ_update import CardapioCategoriaUpdate
from pedidos.views.cardapio_categ_delete import cardapio_categoria_delete

from pedidos.views.cliente_list import ClienteList
from pedidos.views.cliente_create import ClienteCreate
from pedidos.views.cliente_update import ClienteUpdate
from pedidos.views.cliente_delete import cliente_delete

from pedidos.views.complemento_list import ComplementoList
from pedidos.views.complemento_create import ComplementoCreate
from pedidos.views.complemento_update import ComplementoUpdate
from pedidos.views.complemento_delete import complemento_delete

from pedidos.views.grupo_complemento_list import GrupoComplementoList
from pedidos.views.grupo_complemento_create import GrupoComplementoCreate
from pedidos.views.grupo_complemento_update import GrupoComplementoUpdate
from pedidos.views.grupo_complemento_delete import grupo_complemento_delete

from pedidos.views.itens_list import ItensList
from pedidos.views.itens_create import ItensCreate
from pedidos.views.itens_update import ItensUpdate
from pedidos.views.itens_delete import itens_delete

from pedidos.views.itens_pedido_complemento_list import ItensPedidoComplementoList
from pedidos.views.itens_pedido_complemento_create import ItensPedidoComplementoCreate
from pedidos.views.itens_pedido_complemento_update import ItensPedidoComplementoUpdate
from pedidos.views.itens_pedido_complemento_delete import itens_complemento_delete

from pedidos.views.itens_pedido_list import ItensPedidoList
from pedidos.views.itens_pedido_create import ItensPedidoCreate
from pedidos.views.itens_pedido_update import ItensPedidoUpdate
from pedidos.views.itens_pedido_delete import itens_pedido_delete

from pedidos.views.pedido_list import PedidoList
from pedidos.views.pedido_create import PedidoCreate
from pedidos.views.pedido_update import PedidoUpdate
from pedidos.views.pedido_delete import pedido_delete

from pedidos.views.restaurante_list import RestauranteList
from pedidos.views.restaurante_create import RestauranteCreate
from pedidos.views.restaurante_update import RestauranteUpdate
from pedidos.views.restaurante_delete import restaurante_delete

from pedidos.views.tempo_list import TempoEstimadoList
from pedidos.views.tempo_create import TempoEstimadoCreate
from pedidos.views.tempo_update import TempoEstimadoUpdate
from pedidos.views.tempo_delete import tempo_delete




urlpatterns = [
    path('', CadapioList.as_view(), name='list_cardapio'),
    path('novo/', CardapioCreate.as_view(), name='create_cardapio'),
    path('editar/<int:pk>/', CardapioUpdate.as_view(), name='update_cardapio'),
    path('delete/<int:pk>/', cardapio_delete, name='delete_cardapio'),

    path('categoria', CadapioCategoriaList.as_view(), name='list_categoria'),
    path('categoria_novo/', CardapioCategoriaCreate.as_view(), name='create_categoria'),
    path('categoria_editar/<int:pk>/', CardapioCategoriaUpdate.as_view(), name='update_categoria'),
    path('categoria_delete/<int:pk>/', cardapio_categoria_delete, name='delete_categoria'),

    path('cliente', ClienteList.as_view(), name='list_cliente'),
    path('cliente_novo', ClienteCreate.as_view(), name='create_cliente'),
    path('cliente_editar/<int:pk>/', ClienteUpdate.as_view(), name='update_cliente'),
    path('cliente_delete/<int:pk>/', cliente_delete, name='delete_cliente'),

    path('complemento', ComplementoList.as_view(), name='list_complemento'),
    path('complemento_novo', ComplementoCreate.as_view(), name='create_complemento'),
    path('complemento_editar/<int:pk>/', ComplementoUpdate.as_view(), name='update_complemento'),
    path('complemento_delete/<int:pk>/', complemento_delete, name='delete_complemento'),
    
    path('grupo_complemento', GrupoComplementoList.as_view(), name='list_grupo_complemento'),
    path('grupo_complemento_novo', GrupoComplementoCreate.as_view(), name='create_grupo_complemento'),
    path('grupo_complemento_editar/<int:pk>/', GrupoComplementoUpdate.as_view(), name='update_grupo_complemento'),
    path('grupo_complemento_delete/<int:pk>/', grupo_complemento_delete, name='delete_grupo_complemento'),
    
    path('itens', ItensList.as_view(), name='list_itens'),
    path('itens_novo', ItensCreate.as_view(), name='create_itens'),
    path('itens_editar/<int:pk>/', ItensUpdate.as_view(), name='update_itens'),
    path('itens_delete/<int:pk>/', itens_delete, name='delete_itens'),

    path('itens_complemento', ItensPedidoComplementoList.as_view(), name='list_iten_complemento'),
    path('itens_complemento_novo', ItensPedidoComplementoCreate.as_view(), name='create_iten_complemento'),
    path('itens_complemento_editar/<int:pk>/', ItensPedidoComplementoUpdate.as_view(), name='update_iten_complemento'),
    path('itens_complemento_delete/<int:pk>/', itens_complemento_delete, name='delete_iten_complemento'),

    path('itens_pedido', ItensPedidoList.as_view(), name='list_iten_pedido'),
    path('itens_pedido_novo', ItensPedidoCreate.as_view(), name='create_iten_pedido'),
    path('itens_pedido_editar/<int:pk>/', ItensPedidoUpdate.as_view(), name='update_iten_pedido'),
    path('itens_pedido_delete/<int:pk>/', itens_pedido_delete, name='delete_iten_pedido'),

    path('pedido', PedidoList.as_view(), name='list_pedido'),
    path('pedido_novo', PedidoCreate.as_view(), name='create_pedido'),
    path('pedido_editar/<int:pk>/', PedidoUpdate.as_view(), name='update_pedido'),
    path('pedido_delete/<int:pk>/', pedido_delete, name='delete_pedido'),

    path('restaurante', RestauranteList.as_view(), name='list_restaurante'),
    path('restaurante_novo', RestauranteCreate.as_view(), name='create_restaurante'),
    path('restaurante_editar/<int:pk>/', RestauranteUpdate.as_view(), name='update_restaurante'),
    path('restaurante_delete/<int:pk>/', restaurante_delete, name='delete_restaurante'),

    path('tempo', TempoEstimadoList.as_view(), name='list_tempo'),
    path('tempo_novo', TempoEstimadoCreate.as_view(), name='create_tempo'),
    path('tempo_editar/<int:pk>/', TempoEstimadoUpdate.as_view(), name='update_tempo'),
    path('tempo_delete/<int:pk>/', tempo_delete, name='delete_tempo'),

]
