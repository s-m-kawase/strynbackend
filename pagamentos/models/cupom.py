from django.db import models


class Cupom(models.Model):
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome',
    )

    descricao = models.TextField(
        max_length=200,
        verbose_name='Descrição',
        null=True, blank=True
    )

    valor = models.DecimalField(
        verbose_name='Valor',
        max_digits=10,
        decimal_places=2,
        blank=True, null=True
    )

    porcentagem = models.DecimalField(
        verbose_name="porcentagem",
        max_digits=5,
        decimal_places=2,
        blank=True, null=True
        )

    cod_cupom = models.CharField(
        max_length=200,
        verbose_name='Codigo do Cupom',
        null=True,
        unique=True
    )

    validado_ate = models.DateTimeField(
        verbose_name='Validade até',
        null=True
    )

    def calcular_porcentagem_desconto(self):
      if self.valor is not None:
          return int(self.valor)  # Não é necessário multiplicar por 100
      else:
          return 0



    def validar_cupom(self):
        pass

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'pagamentos'
        verbose_name = 'Cupom'
        verbose_name_plural = 'Cupons'
