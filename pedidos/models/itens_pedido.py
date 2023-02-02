from django.db import models
from pedidos.models.item_cardapio import ItemCardapio
from pedidos.models.pedido import Pedidos

class ItensPedido(models.Model):

    item = models.OneToOneField(
        ItemCardapio,
        on_delete=models.SET_NULL,
        verbose_name='Itens',
        null=True
    )

    pedido = models.ForeignKey(
        Pedidos,
        verbose_name="Pedido",
        on_delete=models.SET_NULL,
        null=True
    )

    """ item_complemento = models.ManyToManyField(
        ItensPedidoComplementos,
        verbose_name='Itens de complementos pedido',
        blank=True, null=True,
    ) """

    quantidade = models.IntegerField(
        verbose_name='Quantidade de Produto',
        null=True
    )

    @property
    def total(self):
        
        total = 0
        total = float(self.quantidade) * (float(self.item.preco) if self.item else 0)

        return total

    def calcular_preco(self):
        pass

    def __str__(self):
        return str(self.id)
    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Item Pedido'
        verbose_name_plural = 'Itens Pedidos'
    