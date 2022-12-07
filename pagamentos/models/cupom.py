from django.db import models


class Cupom(models.Model):
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome',
        )

    descricao = models.TextField(
            max_length=200,
            verbose_name='Descrição',
        )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor',
    )

    cod_cupom = models.CharField(
        max_length=200,
        verbose_name='Codigo do Cupom',
        null= True, blank=True
    )

    validado_ate = models.DateField(
        verbose_name='Validade até',
        null= True, blank=True
    )


    def calcular_Preco(self):
        pass



    def validar_cupom(self):
        pass

    def __str__(self):
        return self.nome