from django.db import models
from .produto import Produto


class Price(models.Model):

    produto = models.ForeignKey(
        Produto,
        verbose_name='Produto',
        on_delete=models.CASCADE
    )

    stripe_price_id = models.CharField(
        verbose_name='stripe_preço_id',
        max_length=100
    )

    price = models.IntegerField(
        default=0,
        verbose_name='Preço',
    ) 

    quantidade = models.IntegerField(
        default=1,
        verbose_name='Preço',
    ) 

    def __str__(self):
        return f'{"{0:.2f}".format(self.price / 100)} - {self.produto.produto}'

    class Meta:
        '''Sub classe para definir meta atributos da classe principal.'''

        app_label = 'apistripe'
        verbose_name = 'price'
        verbose_name_plural = 'prices'
