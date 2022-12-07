from django.db import models


class CategoriaCardapio(models.Model):

    nome = models.CharField(
        max_length=40,
        verbose_name='Nome da Categoria',
        blank=True, null=True,
        )

    status = models.BooleanField(
        verbose_name='Está Pausado ?',
        default=False,
    )


    def __str__(self):
         return self.nome
    