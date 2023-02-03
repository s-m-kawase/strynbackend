from django.db import models
from pedidos.models.complemento import Complementos
from pedidos.models.itens_pedido import ItensPedido

class ItensPedidoComplementos(models.Model):
    
    complemento = models.ForeignKey(
        Complementos,
        on_delete=models.SET_NULL,
        verbose_name='Complemento',
        null=True
    )

    item_pedido = models.ForeignKey(
        ItensPedido,
        on_delete=models.SET_NULL,
        verbose_name='Item do Pedido',
        null=True
    )

    quantidade = models.IntegerField(
        verbose_name='Quantidade de Produtos Adicionados',
        null=True
    )

    @property
    def total(self):
        return 0
        #total+= float(self.complemento.) * float(self.quantidade)

    def __str__(self):
        return str(self.complemento)

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Item Pedido Complemento'
        verbose_name_plural = 'Itens Pedidos Complementos'
    