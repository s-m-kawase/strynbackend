from django.db import models



class Cliente(models.Model):
    nome_cliente = models.CharField(
        max_length=200,
        verbose_name='Nome do Cliente',
        blank=True, null=True,
    )

    cpf = models.CharField(
        max_length=14,
        verbose_name="CPF",
    )

    celular = models.CharField(
        max_length=17,
        verbose_name="Numero Celular",
        blank=True,
        null=True,
    )

    historico_pedido = models.ForeignKey(
        'pedidos.Pedidos',
        on_delete=models.CASCADE,
        related_name='historico',
        blank=True, null=True
        
    )

    def __str__(self):
        return self.nome_cliente