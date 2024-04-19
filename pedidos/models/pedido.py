from email.policy import default
from django.db import models
from pedidos.models.tempo import TempoEstimado
from .restaurante import Restaurante
from pagamentos.models.cupom import Cupom
from pagamentos.models.adicional import Adicional
from django.db.models import Sum

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
        ('Aguardando Confirmação', 'Aguardando Confirmação'),
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

    # tempo_estimado = models.ForeignKey(
    #     TempoEstimado,
    #     verbose_name='Tempo Estimado',
    #     on_delete=models.SET_NULL,
    #     blank=True, null=True,
    # )

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
    
    payment_intent_id = models.CharField(
        max_length=500,
        blank=True, null=True
    )

    hash_cliente = models.CharField(
        verbose_name="Hash_cliente",
        max_length=200,
        blank=True, null=True
    )

    cliente_identificado = models.BooleanField(
        verbose_name="cliente cadastrado",
        default=True,
    )

    nome_cliente = models.CharField(
        verbose_name="Nome do cliente",
        max_length=200,
        blank=True, null=True
    )

    email_cliente = models.EmailField(
        verbose_name="E-mail do cliente",
        max_length=254,
        null=True, blank=True
    )

    hora_status_pago = models.DateTimeField(
        verbose_name="Hora que status mudou para pago",
        null=True, blank=True)
    
    hora_status_aguardando_preparo = models.DateTimeField(
        verbose_name="Hora que status mudou para aguardando preparo",
        null=True, blank=True,
    )

    taxa_de_atendimento = models.DecimalField(
        verbose_name="Taxa de atendimento ",
        decimal_places=2,
        max_digits=10,
        default=0,
        blank=True, null=True,
    )


    cpf = models.CharField(
        verbose_name="CPF",
        max_length=14,
        null=True,
        blank=True
    )

    pagamento_asaas = models.CharField(
        max_length=500,
        blank=True, null=True
    )

    # item_pronto = models.BooleanField(
    #     verbose_name="Item pronto",
    #     default=False,
    #     blank=True,null=True
    # )

    @property
    def subtotal(self):
        subtotal = 0

        for item in self.itenspedido_set.all():
            if item.preco_item_mais_complementos is not None:
                subtotal += item.preco_item_mais_complementos
        return subtotal

    # @property
    # def total_split(self):

    #     adicionais = 0
    #     for adicional in self.adicionais.all():
    #         adicionais += float(adicional.valor)

    #     cupom = 0
    #     total = 0
    #     total += float(self.subtotal if self.subtotal else 0)
    #     total -= float(self.desconto if self.desconto else 0)
    #     total += float(adicionais)
    #     # total += float(self.taxa_de_atendimento if self.taxa_de_atendimento else 0)
        

    #     if self.cupom:
    #         if self.cupom.valor_fixo == True:
    #             total = float(total)
    #             print("valor total")
    #             print(total)
    #             print(self.cupom.porcentagem)
    #             total = total - float(self.cupom.porcentagem)
    #             print("valor cupom")
    #             print(cupom)
    #             print(self.cupom.porcentagem)

    #         else:
    #             total = total
    #             taxa = float(self.cupom.porcentagem / 100 ) if self.cupom else 0 
    #             cupom = total * taxa
                
    #         total -= round(float(cupom),2)
            

    #     return round(total, 2)


    @property
    def total(self):

        adicionais = 0
        for adicional in self.adicionais.all():
            adicionais += float(adicional.valor)

        cupom = 0
        total = 0
        total += float(self.subtotal if self.subtotal else 0)
        total -= float(self.desconto if self.desconto else 0)
        total += float(adicionais)
        total += float(self.taxa_de_atendimento if self.taxa_de_atendimento else 0)
        

        if self.cupom:
            if self.cupom.valor_fixo == True:
                total = float(total)
                print("valor total")
                print(total)
                print(self.cupom.porcentagem)
                total = total - float(self.cupom.porcentagem)
                print("valor cupom")
                print(cupom)
                print(self.cupom.porcentagem)

            else:
                total = total
                taxa = float(self.cupom.porcentagem / 100 ) if self.cupom else 0 
                cupom = total * taxa
                
            total -= round(float(cupom),2)
            

        return round(total, 2)
    # @property
    # def total_taxa_servico_no_pedido(self):
    #   taxa = float(self.restaurante.taxa_servico ) if self.restaurante else 0
    #   taxa_total_servico = round(float(self.subtotal) * (taxa/100),2)

    #   context = ({
    #       "porcentagem":taxa,
    #       "taxa_de_servico":taxa_total_servico
    #   })
    #   return context

    @property
    def itens_quantidade(self):
        quantidade = 0
        for item in self.itenspedido_set.all():
            quantidade+=item.quantidade if item.quantidade else 0

        return quantidade

    @property
    def valor_pago(self):
        self.pagamento_set.all().aggregate(valor=Sum('valor_pago'))['valor']

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
        return str(self.id) if self.id else f'{self.id}'
    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'