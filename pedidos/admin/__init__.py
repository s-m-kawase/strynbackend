from pedidos.admin.cardapio_admin import CardapioAdmin 
from pedidos.admin.categoria_cardapio_admin import CategoriaCardapioAdmin
from pedidos.admin.cliente_admin import ClienteAdmin
from pedidos.admin.complemento_admin import ComplementosAdmin
from pedidos.admin.grupo_complemento_admin import GrupoComplementosAdmin
from pedidos.admin.item_cardapio_admin import ItemCardapioAdmin
from pedidos.admin.itens_pedido_complementos_admin import ItensPedidoComplementosAdmin
from pedidos.admin.itens_pedido_admin import ItensPedidoAdmin
from pedidos.admin.restaurante_admin import RestauranteAdmin
from pedidos.admin.tempo_admin import TempoEstimadoAdmin
from .pedido_admin import PedidosAdmin



__all__ = [
    CardapioAdmin,
    CategoriaCardapioAdmin,
    ClienteAdmin,
    ComplementosAdmin,
    GrupoComplementosAdmin,
    ItemCardapioAdmin,
    ItensPedidoComplementosAdmin,
    ItensPedidoAdmin,
    RestauranteAdmin,
    TempoEstimadoAdmin,
    PedidosAdmin,
]
