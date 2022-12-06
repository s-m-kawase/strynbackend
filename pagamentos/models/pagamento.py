from django.db import models
from pagamentos.models.cupom import Cupom
from pagamentos.models.adicional import Adicional


class Pagamento(models.Model):
    codigo_pagamento = models.CharField(
        max_length=100,
        verbose_name='Cóigo do pagamento',
        null= True, blank=True    
        )

    tipos_choice = (
        ('Pagar na mesa', 'Nome da opção'),
        ('Vale refeição', 'Nome da opção'),
        ('Vale-alimentação', 'Nome da opção'),
        ('Pagar com pix,', 'Nome da opção'),
        ('Cartão de crédito', 'Nome da opção'),
        ('Cartão de debito', 'Nome da opção'),
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

    def calcular_preco(self):
        pass
    

def __str__(self):
    return self.codigo_pagamento

