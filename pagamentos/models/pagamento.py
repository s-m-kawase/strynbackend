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
        ('Pagar na mesa', 'Pagar na mesa'),
        ('Vale refeição', 'Vale refeição'),
        ('Vale-alimentação', 'Vale-alimentação'),
        ('Pagar com pix', 'Pagar com pix'),
        ('Cartão de crédito', 'Cartão de crédito'),
        ('Cartão de debito', 'Cartão de debito'),
    )

    pagamento = models.CharField(
        verbose_name="Tipo pagamento",
        choices=TIPO_CHOICE,
        max_length=50,
        default="Cartão de debito"
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

    
    @property
    def total(self):
        
        return self.pedido.subtotal

    def __str__(self):
        return self.pagamento

    class Meta:
        app_label = 'pagamentos'
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
