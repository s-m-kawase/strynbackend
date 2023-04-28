from django.db import models


class CategoriaCardapio(models.Model):

    nome = models.CharField(
        max_length=40,
        verbose_name='Nome da Categoria',
        null=True,
        unique=True
    )

    status = models.BooleanField(
        verbose_name='Está pausado ?',
        default=False
    )

    em_promocao = models.BooleanField(
        verbose_name="Está na Promoção?",
        default=False
    )

    ordem =  models.IntegerField(
        verbose_name='Ordem',
        null=True, blank=False)


    def __str__(self):
        return self.nome
    

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Categoria Cardapio'
        verbose_name_plural = 'Categorias Cardapios'
    