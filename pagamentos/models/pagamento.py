import json
from django.db import models
from pedidos.models.pedido import Pedidos

class Pagamento(models.Model):
    codigo_pagamento = models.CharField(
        max_length=100,
        verbose_name='Código do pagamento',
        null= True,
        unique=True
    )

    TIPO_CHOICE = (
        ('Pagamento na mesa', 'Pagamento na mesa'),
        ('Pagamento online', 'Pagamento online'),
    )

    pagamento = models.CharField(
        verbose_name="Tipo pagamento",
        choices=TIPO_CHOICE,
        max_length=50,
        default="Pagamento na mesa"
    )

    pedido = models.ForeignKey(
        Pedidos,
        verbose_name="Pedido",
        on_delete=models.SET_NULL,
        null=True
    )

    valor_pago = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor Pago',
        null=True,
        default=0
    )
    payment_details = models.TextField(
        null=True,
        blank=True,
        verbose_name='Detalhes do pagamento'
    )

    @property
    def total(self):

        return self.pedido.subtotal

    def __str__(self):
        return self.pagamento

    class Meta:
        app_label = 'pagamentos'
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
