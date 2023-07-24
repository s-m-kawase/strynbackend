from django.db import models


class Adicional(models.Model):
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome",
        null= True
    )

    descricao = models.TextField(
        max_length=200,
        verbose_name="Descrição",
        null=True,
        blank=True
    )

    valor = models.DecimalField(
        verbose_name="Valor",
        max_digits=10,
        decimal_places=2
    )


    def calcular_preco(self):
        pass

    def __str__(self):
        return f'{self.nome} - R${self.valor}' if f'{self.nome} - R${self.valor}' else f'{self.id}'
    
    class Meta:
        app_label = 'pagamentos'
        verbose_name = 'Adicional'
        verbose_name_plural = 'Adicionais'
