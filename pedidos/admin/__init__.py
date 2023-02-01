from pedidos.admin.cardapio_admin import CardapioAdmin 
from pedidos.admin.categoria_cardapio_admin import CategoriaCardapioAdmin
from pedidos.admin.cliente_admin import ClienteAdmin
from pedidos.admin.complemento_admin import ComplementosAdmin
from pedidos.admin.grupo_complemento_admin import GrupoComplementosAdmin
from pedidos.admin.item_cardapio_admin import ItemCardapioAdmin
from pedidos.admin.itens_pedido_complementos_admin import ItensPedidoComplementosAdmin
from pedidos.admin.itens_pedido_admin import ItensPedidoAdmin
from pedidos.admin.itens_pedido_inline import ItensPedidoInline
from pedidos.admin.restaurante_admin import RestauranteAdmin
from pedidos.admin.tempo_admin import TempoEstimadoAdmin
from pedidos.admin.pedido_admin import PedidosAdmin
from pedidos.admin.pedidos_inline import PedidosInline



__all__ = [
    CardapioAdmin,
    CategoriaCardapioAdmin,
    ClienteAdmin,
    ComplementosAdmin,
    GrupoComplementosAdmin,
    ItemCardapioAdmin,
    ItensPedidoComplementosAdmin,
    ItensPedidoAdmin,
    ItensPedidoInline,
    RestauranteAdmin,
    TempoEstimadoAdmin,
    PedidosAdmin,
    PedidosInline
]
