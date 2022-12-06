from django.db import models
from pedidos.models.tempo import TempoEstimado
from pedidos.models.iten import Item


class Pedido(models.Model):

    numero_pedido = models.IntegerField(
        verbose_name='Número do Pedido',
        blank=True, null=True,
    )

    data_criacao = models.DateField(
        verbose_name='Data da Criação',
        auto_now=True,
    ) 
    
    status_pedido = (
        ('Solicitado','solicitado'),
        ('Entregue','entregue'),
        ('Concluído','concluido'),
        ('Cancelado','cancelado'),
    )

    tempo_estimado = models.ForeignKey(
        TempoEstimado,
        on_delete=models.CASCADE,
        verbose_name='Tempo Estimado',
        blank=True, null=True,
    )

    numero_mesa = models.IntegerField(
        verbose_name="Númedo da Mesa",
        blank=True, null=True,
    )

    itens = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name='Itens',
        blank=True, null=True,
    )

    sub_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Subtotal do Pedido',
        blank=True, null=True       
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor total do Pedido"
    )

    cliente = models.ForeignKey(
        'pedidos.Cliente',
        on_delete=models.CASCADE,
        verbose_name='Cliente',
        blank=True, null=True,
    )



    def efetuar_pedido(self):
        pass


    def adicionar_item(self):
        pass


    def adicionar_complemento(self):
        pass

    def atualizar_quantidade(self):
        pass

    def ver_detalhe_pedido(self):
        pass

    def finalizr_pedido(self):
        pass

    def __str__(self):
        return str(self.numero_pedido)
