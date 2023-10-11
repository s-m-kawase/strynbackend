from django.db import models
from django.contrib.auth.models import User
from .tempo import TempoEstimado
from pedidos.models.categoria_cardapio import CategoriaCardapio


class Restaurante(models.Model):

    nome = models.CharField(
        max_length=90,
        verbose_name='Nome do Restaurante',
        null=True,
    )

    usuario = models.ManyToManyField(
        User,
        verbose_name='Usuários',
        blank=True, null=True
    )

    categoria = models.ForeignKey(
        CategoriaCardapio,
        on_delete=models.SET_NULL,
        verbose_name='Categoria do Cardápio',
        blank=True, null=True,
    )

    descricao = models.TextField(
        max_length=1000,
        verbose_name="Descrição do Restaurante",
        blank=True, null=True
    )

    logo = models.ImageField(
        verbose_name='Logo do Restaurante',
        blank=True, null=True,
    )

    baner = models.ImageField(
        verbose_name='Banner do Restaurante',
        blank=True, null=True,
    )

    total_mesa = models.IntegerField(
        verbose_name="Total de Mesas",
        blank=True, null=True,
    )

    horario_abertura = models.TimeField(
        verbose_name='Horário de Abertura',
        blank=True, null=True,
    )

    horario_encerramento = models.TimeField(
        verbose_name='Horário de Encerramento',
        blank=True, null=True,
    )
    tempo_estimado = models.ForeignKey(
        TempoEstimado,
        verbose_name='Tempo Estimado',
        on_delete=models.SET_NULL,
        blank=True, null=True,
    )

    # taxa_servico = models.IntegerField(
    #     verbose_name="Taxa de serviço em porcentagem",
    #     blank=True, null=True,
    #     default=10
    # )

    link_restaurante = models.TextField(
        verbose_name="QR code Restaurante",
        null=True, blank=True,
    )

    num_obrigatorio = models.BooleanField(
        verbose_name="Número da mesa é obrigatório? ",
        default=False
    )

    razao_social = models.CharField(
        max_length=255,
        verbose_name="Razão Social",
        blank=True, null=True,
    )

    cnpj = models.CharField(
        max_length=14,
        verbose_name="CNPJ",
        blank=True, null=True,
    )

    rua = models.CharField(
        max_length=255,
        verbose_name="Rua",
        blank=True, null=True
    )

    numero = models.CharField(
        max_length=10,
        verbose_name="Número",
        blank=True, null=True
    )

    complemento = models.CharField(
        max_length=255,
        verbose_name="Complemento",
        blank=True, null=True
    )

    bairro = models.CharField(
        max_length=255,
        verbose_name="Bairro",
        blank=True, null=True
    )

    cep = models.CharField(
        max_length=8,
        verbose_name="CEP",
        blank=True, null=True
    )

    UF_CHOICE = (
        ('AC', 'AC'),
        ('AL', 'AL'),
        ('AP', 'AP'),
        ('AM', 'AM'),
        ('BA', 'BA'),
        ('CE', 'CE'),
        ('DF', 'DF'),
        ('ES', 'ES'),
        ('GO', 'GO'),
        ('MA', 'MA'),
        ('MT', 'MT'),
        ('MS', 'MS'),
        ('MG', 'MG'),
        ('PA', 'PA'),
        ('PB', 'PB'),
        ('PR', 'PR'),
        ('PE', 'PE'),
        ('PI', 'PI'),
        ('RR', 'RR'),
        ('RO', 'RO'),
        ('RJ', 'RJ'),
        ('RN', 'RN'),
        ('RS', 'RS'),
        ('SC', 'SC'),
        ('SP', 'SP'),
        ('SE', 'SE'),
        ('TO', 'TO'),
    )

    uf = models.CharField(
        verbose_name='UF',
        choices=UF_CHOICE,
        max_length=2,
        default='AC'
    )

    cidade = models.CharField(
        max_length=255,
        verbose_name="Cidade",
        blank=True, null=True
    )

    inscricao_estadual = models.CharField(
        max_length=255,
        verbose_name="Inscricão Estadual",
        blank=True, null=True
    )

    inscricao_municipal = models.CharField(
        max_length=255,
        verbose_name="Inscrição Municipal",
        blank=True, null=True
    )

    agencia = models.CharField(
        max_length=6,
        verbose_name="Agência",
        blank=True, null=True
    )

    conta = models.CharField(
        max_length=9,
        verbose_name="Conta",
        blank=True, null=True
    )

    digito = models.CharField(
        max_length=1,
        verbose_name="Dígito",
        blank=True, null=True
    )

    banco = models.CharField(
        max_length=255,
        verbose_name="Banco",
        blank=True, null=True
    )

    cvc = models.CharField(
        max_length=3,
        verbose_name="CVC",
        blank=True, null=True
    )

    tempo_ideal = models.TimeField(
        verbose_name= 'Tempo Bom',
        blank=True, null=True,
    )

    tempo_medio = models.TimeField(
        verbose_name= 'Tempo Médío',
        blank=True, null=True,
    )

    tempo_limite = models.TimeField(
        verbose_name= 'Tempo Limite',
        blank=True, null=True,
    )

    chave_connect = models.CharField(
        verbose_name="Chave Connect do Stripe",
        blank=True, null=True,
        max_length=50
    )

    pocentagem_para_tranferencia = models.DecimalField(
        verbose_name='Valor em porcentagem que será enviado ao restaurante',
        max_digits=10,
        default=90,
        decimal_places=2,
        blank=True, null=True
    )

    chave_asaas = models.CharField(
        verbose_name="Chave Connect do Asaas",
        blank=True, null=True,
        max_length=50
    )

    # pedido_no_seu_restaurante = models.BooleanField(
    #     verbose_name="Pedido No meu Restaurante",
    #     default=False
    # )

    @property
    def passar_porcentagem_em_decimal(self):
        return self.pocentagem_para_tranferencia / 100


    def __str__(self):
        return self.nome if self.nome else f'{self.id}'

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'
