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

    ordem = models.AutoField(default=1, primary_key=True, serialize=False, verbose_name='Ordem categoria'),
        

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Categoria Cardapio'
        verbose_name_plural = 'Categorias Cardapios'
    