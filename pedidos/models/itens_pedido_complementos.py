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
        on_delete=models.CASCADE,
        verbose_name='Item do Pedido',
        null=True
    )

    quantidade = models.IntegerField(
        verbose_name='Quantidade de Produtos Adicionados',
        null=True
    )
    
    valor_unitario = models.DecimalField(
        verbose_name='Valor Unitário',
        max_digits=10,
        decimal_places=2,
        blank=True, null= True,
    )
    
    valor_total = models.DecimalField(
        verbose_name='Valor Total',
        max_digits=10,
        decimal_places=2,
        blank=True, null= True,
    )

    
    def calcular_valor_total_complemento(self):
        self.valor_unitario = float(self.complemento.preco)
        self.valor_total = self.valor_unitario * float(self.quantidade)
        self.save()

    def __str__(self):
        return f'{self.item_pedido} - {self.complemento}' if self.item_pedido and self.complemento else f'{self.id}'

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Item Pedido Complemento'
        verbose_name_plural = 'Itens Pedidos Complementos'
    