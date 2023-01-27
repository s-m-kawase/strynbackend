from django.db import models
from pedidos.models.item_cardapio import ItemCardapio
from pedidos.models.complemento import Complementos


class ItensPedido(models.Model):

    item = models.ForeignKey(
        ItemCardapio,
        on_delete=models.CASCADE,
        verbose_name='Itens',
        blank=True, null=True,
    )


    quantidade = models.IntegerField(
        verbose_name='Quantidade de Produto',
        blank=True, null=True,
    )

    valor_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor Unitario',
        blank=True, null=True,
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor total do Pedido',
        blank=True, null=True,
    )

    complementos = models.ForeignKey(
        Complementos,
        on_delete=models.CASCADE,
        verbose_name='Complementos',
        blank=True, null=True,

    )

    def calcular_preco(self):
        pass

    def __str__(self):
        return str(self.item)
    