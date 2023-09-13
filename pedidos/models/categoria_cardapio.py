from django.db import models


class CategoriaCardapio(models.Model):

    nome = models.CharField(
        max_length=40,
        verbose_name='Nome da Categoria',
        null=True,
    )

    status = models.BooleanField(
        verbose_name='Está pausado ?',
        default=False
    )

    em_promocao = models.BooleanField(
        default=False,
        verbose_name='Em promoção ?'
    )

    

    def save(self, *args, **kwargs):
        if self.em_promocao is None:
            self.em_promocao = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome    if self.nome else f'{self.id}'

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Categoria Cardapio'
        verbose_name_plural = 'Categorias Cardapios'
    