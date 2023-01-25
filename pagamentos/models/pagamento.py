from django.db import models
from pagamentos.models.cupom import Cupom
from pagamentos.models.adicional import Adicional


class Pagamento(models.Model):
    codigo_pagamento = models.CharField(
        max_length=100,
        verbose_name='Cóigo do pagamento',
        null= True, blank=True    
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

    desconto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor do Desconto'
    )

    adicionais = models.ForeignKey(
        Adicional,
         on_delete=models.CASCADE,
        verbose_name='Adicionais',
        null= True, blank=True    
        )

    cupom = models.ForeignKey(
        Cupom,
         on_delete=models.CASCADE,
        verbose_name='Cupom',
        null= True, blank=True    
        )

    # def calcular_preco(self):
    #     pass
    

    def __str__(self):
        return self.pagamento

