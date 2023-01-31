from django.db import models
from pedidos.models.complemento import Complementos


class ItensPedidoComplementos(models.Model):
    
    complemento = models.ManyToManyField(
        Complementos,
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

    # @property
    # def total_get(self):
    #     from .itens_pedido import ItensPedido
    #     items = ItensPedido.objects.itenspedidocomplementos_set.all()
    #     qtd = 0
    #     unitario= []
    #     for item in items:
    #         qtd += item.quantidade
            
    #         unitario.append({
    #             "quantidade": qtd,
    #             "valor_unitario":item.valor_unitario,
    #             "sub_total":qtd * item.valor_unitario,
    #         })
    #     return unitario

    def __str__(self):
        return str(self.complemento)
    