from django.db import models
from pedidos.models.complemento import Complementos


class ItensPedidoComplementos(models.Model):
    
    complemento = models.ForeignKey(
        Complementos,
        on_delete=models.CASCADE,
        verbose_name='Complemento',
        blank=True, null=True,
    )

    quantidade = models.IntegerField(
        verbose_name='Quantidade de Produtos Adicionados',
        blank=True, null=True,   
    )

    valor_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor unitario do Produto',
        blank=True, null=True,
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="valor total dos Produtos Adicionados",
        blank=True, null=True,
    )

    def calcular_preco(self):
        pass

    def __str__(self):
        return str(self.complemento)
    