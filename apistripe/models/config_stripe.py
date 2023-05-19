from django.db import models


class ConfigStripe(models.Model):
    
    nome = models.CharField(
        verbose_name='Nome',
        max_length=100,
    )

    token = models.CharField(
        verbose_name='Secret Key Stripe',
        max_length=100
    )

    def __str__(self):
        '''Método que retorna a representação do objeto como string.'''
        return self.nome

    class Meta:
        '''Sub classe para definir meta atributos da classe principal.'''

        app_label = 'apistripe'
        verbose_name = 'configuração stripe'
        verbose_name_plural = 'configurações Stripe'