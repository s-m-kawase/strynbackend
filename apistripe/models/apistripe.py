from django.db import models

class ApiStripe(models.Model):

    prices_strip = models.CharField(
        verbose_name='Prices id do Strip',
        max_length=100,
        blank=True , null= True
    )
    
    quantidade = models.CharField(
        verbose_name='quantidade',
        max_length=20,
        blank=True , null= True
    )

    FORMA_PAGAMENTO = (
        ('Cartao Credito','Cartao Credito'),
        ('Cartao Debito','Cartao Debito'),
        ('Pix','Pix'),
        ('Pic Pay','Pic Pay'),
    )

    forma_pagamento = models.CharField(
        verbose_name="Status do Pedido",
        choices=FORMA_PAGAMENTO,
        default='Cartao Credito',
        max_length=30
    )
    
    url_sucesso = models.CharField(
        verbose_name='Url sucesso',
        max_length=100,
        blank=True , null= True
    )

    url_cancelamento = models.CharField(
        verbose_name='Url cancelamento',
        max_length=100,
        blank=True , null= True
    )


    def __str__(self):
        return str(self.prices_strip)

    
