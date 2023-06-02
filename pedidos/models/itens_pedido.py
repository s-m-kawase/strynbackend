from django.db import models
from pedidos.models.item_cardapio import ItemCardapio
from pedidos.models.pedido import Pedidos


class ItensPedido(models.Model):

    item = models.ForeignKey(
        ItemCardapio,
        on_delete=models.SET_NULL,
        verbose_name='Itens',
        null=True
    )

    pedido = models.ForeignKey(
        Pedidos,
        verbose_name="Pedido",
        on_delete=models.CASCADE,
        null=True
    )

    # item_complemento = models.ManyToOneRel(
    #     ItensPedidoComplementos,
    #     verbose_name='Itens de complementos pedido',
    #     blank=True, null=True,
    # )

    quantidade = models.IntegerField(
        verbose_name='Quantidade de Produto',
        null=True
    )
    
    preco = models.DecimalField(
        verbose_name="Preço Item + Complementos",
        decimal_places=2,
        max_digits=12,
        blank=True, null=True,
    )
    
    multiplicador_item_pedido = models.IntegerField(
        verbose_name='Multiplicador Item Pedido',
        max_length=5,
        default=1,
        blank=True, null=True,
    )

    @property
    def total_item(self):
        
        total = 0
        if self.item:
            total = float(self.quantidade) * (float(self.item.preco) if self.item else 0)

        return total
    
    @property
    def total_complementos(self):
        total = 0
        for complemento in self.itenspedidocomplementos_set.all():
            total += complemento.total
        return total

    def calcular_preco(self):
        try:
            if self.multiplicador_item_pedido != 1:
                self.preco = (self.total_item + self.total_complementos) * self.multiplicador_item_pedido
            else:
                self.preco = self.total_item + self.total_complementos
            self.save()
        except:
            self.preco = 0
            self.save()

    def __str__(self):
        return str(self.item)
    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Item Pedido'
        verbose_name_plural = 'Itens Pedidos'
    