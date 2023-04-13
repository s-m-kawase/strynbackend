from django.db import models


class Complementos(models.Model):

    nome = models.CharField(
        verbose_name='Nome do Complemento',
        max_length=40,
        null=True
    )

    codigo_complemento = models.CharField(
        max_length=40,
        verbose_name='Código do Complemento',
        blank=True,null=True,
        
    )

    descricao = models.TextField(
        max_length=1000,
        verbose_name='Descrição do Complemento',
        blank=True, null=True,
    )

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Preço do Complemento',
        null=True,
    )

    foto = models.ImageField(
        verbose_name='Foto',
        null=True,
    )

    status_venda = models.BooleanField(
        verbose_name="Está Pausado ?",
        default=False,
    )


    def __str__(self):
        return f'{self.nome}'

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Complemento'
        verbose_name_plural = 'Complementos'
    