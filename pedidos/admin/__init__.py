from pedidos.admin.cardapio_admin import CardapioAdmin 
from pedidos.admin.categoria_cardapio_admin import CategoriaCardapioAdmin
from pedidos.admin.cliente_admin import ClienteAdmin
from pedidos.admin.complemento_admin import ComplementosAdmin
from pedidos.admin.grupo_complemento_admin import GrupoComplementosAdmin
from pedidos.admin.iten_admin import ItemAdmin
from pedidos.admin.itens_pedido_complementos_admin import ItensPedidoComplementosAdmin
from pedidos.admin.itens_pedido_admin import IntensPedidoAdmin
from pedidos.admin.restaurante_admin import RestauranteAdmin
from pedidos.admin.tempo_admin import TempoEstimadoAdmin



__all__ = [
    CardapioAdmin,
    CategoriaCardapioAdmin,
    ClienteAdmin,
    ComplementosAdmin,
    GrupoComplementosAdmin,
    ItemAdmin,
    ItensPedidoComplementosAdmin,
    IntensPedidoAdmin,
    RestauranteAdmin,
    TempoEstimadoAdmin,
]
