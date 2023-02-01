__author__ = "Francisco Flávio Nogueira da Silva"
__copyright__ = "Copyright 2020, Flávio Silva"
__credits__ = ["Outbox Sistemas"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Francisco Flávio Nogueira da Silva"
__email__ = "flavio981895788@gmail.com"
__status__ = "Production"


from django.db import models
from django.contrib.auth.models import User
from .destinatario import Destinatario
from djrichtextfield.models import RichTextField

class TemplateEmail(models.Model):
    """
    Classe que serve para o usuário fazer o template do seu email
    """
    assunto = models.CharField(
        max_length = 200,
        verbose_name = "Assunto"
    )

    titulo_email = models.CharField(
        max_length = 200,
        verbose_name = "Título do email"
    )

    legenda_email = models.CharField(
        max_length = 200,
        verbose_name = "Legenda do email",
        blank=True, null=True
    )

    titulo_alteracao_email = models.CharField(
        max_length = 200,
        verbose_name = "Título alteração do email",
        blank=True, null=True
    )

    corpo_email = RichTextField(
        verbose_name = "Corpo do email"
    )

    codigo = models.CharField(
        max_length = 50,
        verbose_name = "Código",
        unique = True
    )

    enviar_usuario_criacao = models.BooleanField(
        verbose_name = "Enviar usuário de criação"
    )

    destinatarios = models.ManyToManyField(
        Destinatario,
        verbose_name="Destinatários",
        blank=True
    )

    def __str__(self):
        return self.assunto

    class Meta:
        app_label = "emails"
        verbose_name = "Template do email"
        verbose_name_plural = "Templates dos emails"
