from django.db import models


class Stripe(models.Model):

    webhook = models.TextField(
        verbose_name='webhook',
    )

    def __str__(self):
        '''Método que retorna a representação do objeto como string.'''
        return self.webhook

    class Meta:
        '''Sub classe para definir meta atributos da classe principal.'''

        app_label = 'apistripe'
        verbose_name = 'Stripe'
        verbose_name_plural = 'Stripes'
