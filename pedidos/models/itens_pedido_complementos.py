from django.db import models
from pedidos.models.complemento import Complementos


class ItensPedidoComplementos(models.Model):
    
    complemento = models.ManyToManyField(
        Complementos,
        verbose_name='Complemento',
        null=True,
        blank=True
    )

    quantidade = models.IntegerField(
        verbose_name='Quantidade de Produtos Adicionados',
        null=True
    )

    valor_unitario = models.DecimalField(
        verbose_name='Valor unitário do Produto',
        max_digits=10,
        decimal_places=2,
        null=True
    )

    @property
    def total(self):
        
        return float(self.valor_unitario) * float(self.quantidade)

    def __str__(self):
        return str(self.complemento)

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Item Pedido Complemento'
        verbose_name_plural = 'Itens Pedidos Complementos'
    