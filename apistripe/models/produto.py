from django.db import models


class Produto(models.Model):

    produto = models.CharField(
        verbose_name='Nome',
        max_length=100,
    )

    strip_produto_id = models.CharField(
        verbose_name='Stripe Produto Id',
        max_length=100
    )

    def __str__(self):
        '''Método que retorna a representação do objeto como string.'''
        return self.produto

    class Meta:
        '''Sub classe para definir meta atributos da classe principal.'''

        app_label = 'apistripe'
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
