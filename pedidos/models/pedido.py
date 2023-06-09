from django.db import models
from pedidos.models.tempo import TempoEstimado
from .restaurante import Restaurante
from pagamentos.models.cupom import Cupom
from pagamentos.models.adicional import Adicional

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
        ('Sacola','Sacola'),
        ('Aguardando Pagamento Mesa', 'Aguardando Pagamento Mesa'),
        ('Pago','Pago'),
        ('Aguardando Preparo', 'Aguardando Preparo'),
        ('Em preparo','Em preparo'),
        ('Concluído','Concluído'),
        ('Cancelado','Cancelado'),
        ('Com erro', 'Com erro'),
        ('Estornado', 'Estornado')
    )

    status_pedido = models.CharField(
        verbose_name="Status do Pedido",
        choices=STATUS_CHOICE,
        default='Sacola',
        max_length=25
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

    desconto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor do Desconto',
        null=True,
        default=0
    )

    cupom = models.ForeignKey(
        Cupom,
        on_delete=models.SET_NULL,
        verbose_name='Cupom',
        null=True,
        blank=True
    )

    adicionais = models.ManyToManyField(
        Adicional,
        verbose_name='Adicionais',
        null= True, blank=True    
    )

    session_id = models.CharField(
        max_length=100,
        blank=True, null=True
    )

    checkou_url=models.CharField(
        max_length=500,
        blank=True, null=True
    )
    payment_intent_id = models.CharField(
        max_length=500,
        blank=True, null=True
    )

    @property
    def subtotal(self):
        subtotal = 0
        
        for item in self.itenspedido_set.all():
            if item.preco_item_mais_complementos is not None:
                subtotal += item.preco_item_mais_complementos
        return subtotal
        
        
        

    @property
    def total(self):
        
        adicionais = 0
        for adicional in self.adicionais.all():
            adicionais += float(adicional.valor)

        taxa_atendimento = 0
        if self.restaurante and self.restaurante.taxa_serviço:
            taxa_atendimento = float(self.restaurante.taxa_serviço / 100)

        cupom = float(self.cupom.valor) if self.cupom else 0

        total = 0
        total += float(self.subtotal if self.subtotal else 0)
        total -= float(self.desconto if self.desconto else 0) 
        total -= float(cupom)
        total += float(adicionais)
        total += float(total * taxa_atendimento)

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
