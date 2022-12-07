from django.db import models


class Adicional(models.Model):
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome",
        null= True, blank=True
    )

    descricao = models.TextField(
        max_length=200,
        verbose_name="Descrição"
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )


    def calcular_preco(self):
        pass

    def __str__(self):
        return self.nome
    