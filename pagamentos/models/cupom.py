from django.db import models
from django.utils import timezone

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
        verbose_name='porcentagem do cupom',
        max_digits=10,
        decimal_places=2,
        blank=True, null=True
    )

    # porcentagem = models.DecimalField(
    #     verbose_name="porcentagem",
    #     max_digits=5,
    #     decimal_places=2,
    #     blank=True, null=True
    #     )

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

    STATUS_CHOICES = (
        ('Valido', 'Valido'),
        ('Utilizado', 'Utilizado'),
        ('Expirado', 'Expirado'),
    )

    status_cupom = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Valido'
    )

    restaurante = models.ForeignKey(
        'pedidos.Restaurante',
        on_delete=models.SET_NULL,
        verbose_name='Restaurante',
        null=True, blank=True
    )

    def aplicar_cupom(self, pedido):
        if self.status_cupom == 'Valido' and self.validado_ate >= timezone.now():
            self.save()
            pedido.cupom = self
            pedido.save()
            return True
        else:
            return False

    def marcar_expirado(self):
        if self.status_cupom == 'Valido' and self.validado_ate < timezone.now():
            self.status_cupom = 'Expirado'
            self.save()



    def valido_para_aplicar(self):
        return self.status_cupom == 'Valido' and self.validado_ate >= timezone.now()

    def __str__(self):
        return self.nome if self.nome else f'{self.id}'

    class Meta:
        app_label = 'pagamentos'
        verbose_name = 'Cupom'
        verbose_name_plural = 'Cupons'
