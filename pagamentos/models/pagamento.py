from django.db import models
from pagamentos.models.cupom import Cupom
from pagamentos.models.adicional import Adicional
from pedidos.models.pedido import Pedidos

class Pagamento(models.Model):
    codigo_pagamento = models.CharField(
        max_length=100,
        verbose_name='Cóigo do pagamento',
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

    desconto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor do Desconto',
        null=True,
        default=0
    )

    adicionais = models.ManyToManyField(
        Adicional,
        verbose_name='Adicionais',
        null= True, blank=True    
    )

    cupom = models.ForeignKey(
        Cupom,
         on_delete=models.SET_NULL,
        verbose_name='Cupom',
        null= True, blank=True
    )

    pedido = models.ForeignKey(
        Pedidos,
        verbose_name="Pedido",
        on_delete=models.SET_NULL,
        null=True
    )

    # def calcular_preco(self):
    #     pass
    
    @property
    def total(self):

        adicionais = 0
        for adicional in self.adicionais_set.all():
            adicionais +=adicional.valor

        cupons = 0
        for cupom in self.cupom_set.all():
            cupons +=cupom.valor

        total = 0
        total += float(self.pedidos.total if self.pedidos else 0)
        total -= float(self.desconto)
        total -= float(cupons)
        total += float(adicionais)

        return total

    def __str__(self):
        return self.pagamento

    class Meta:
        app_label = 'pagamentos'
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
