from django.db import models
from pedidos.models.tempo import TempoEstimado
from .restaurante import Restaurante

class Pedidos(models.Model):

    data_criacao = models.DateTimeField(
        verbose_name='Data da Criação',
        auto_now_add=True,
        blank=True, null=True,
    ) 

    data_atualizacao = models.DateTimeField(
        verbose_name='Data de Atualização',
        auto_now=True,
        blank=True, null=True,
    ) 
    
    STATUS_CHOICE = (
        ('Solicitado','Solicitado'),
        ('Entregue','Entregue'),
        ('Concluído','Concluído'),
        ('Cancelado','Cancelado'),
    )

    status_pedido = models.CharField(
        verbose_name="Status do Pedido",
        choices=STATUS_CHOICE,
        default='Solicitado',
        max_length=20
    )

    tempo_estimado = models.ManyToManyField(
        TempoEstimado,
        verbose_name='Tempo Estimado',
        blank=True, null=True,
    )

    numero_mesa = models.IntegerField(
        verbose_name="Númedo da Mesa",
        blank=True, null=True,
    )

    cliente = models.ForeignKey(
        'pedidos.Cliente',
        on_delete=models.CASCADE,
        verbose_name='Cliente',
        blank=True, 
        null=True
    )

    restaurante = models.ForeignKey(
        Restaurante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    @property
    def subtotal(self):
        subtotal = 0
        for pagamento in self.pagamento_set.all():
            subtotal += pagamento.total

        return subtotal

    @property
    def total(self):
        
        total = 0
        for item in self.itenspedido_set.all():
            total += item.total
        
        return total

    @property
    def itens_quantidade(self):
        quantidade = 0
        for item in self.itenspedido_set.all():
            quantidade+=item.quantidade if item.quantidade else 0

        return quantidade

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
        return str(self.id)
    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
