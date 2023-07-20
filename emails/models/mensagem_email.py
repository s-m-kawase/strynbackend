from crum import get_current_user
from decouple import config
from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.template import Context, Template
from django.template.loader import render_to_string
from django_quill.fields import QuillField

from .destinatario import Destinatario
from .template_email import TemplateEmail


class MensagemEmail(models.Model):
    template_email = models.ForeignKey(
        TemplateEmail,
        verbose_name="Template do email",
        on_delete=models.CASCADE,
    )

    enviado = models.BooleanField(
        verbose_name="Enviado",
        default=False,
    )

    created_by = models.ForeignKey(
        "auth.User",
        related_name="%(class)s_requests_created",
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL,
    )

    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de criação",
    )

    # Campos para histórico
    assunto = models.CharField(
        max_length=200,
        verbose_name="Assunto",
        null=True,
    )

    titulo_email = models.CharField(
        max_length=200,
        verbose_name="Título do email",
        null=True,
    )

    legenda_email = models.CharField(
        max_length=200,
        verbose_name="Legenda do email",
        blank=True,
        null=True,
    )

    titulo_alteracao_email = models.CharField(
        max_length=200,
        verbose_name="Título alteração do email",
        blank=True,
        null=True,
    )

    corpo_email = QuillField(
        verbose_name="Corpo do email",
        null=True,
    )

    corpo_email_text = models.CharField(
        max_length=200,
        verbose_name="Corpo do email em texto",
        null=True,
    )

    codigo = models.CharField(
        max_length=50,
        verbose_name="Código",
        null=True,
    )

    enviar_usuario_criacao = models.BooleanField(
        verbose_name="Enviar usuário de criação",
        default=False,
    )

    destinatarios = models.ManyToManyField(
        Destinatario,
        verbose_name="Destinatários",
        blank=True,
    )

    def gerar_historico(self):
        """
        Gera um histórico da mensagem de e-mail.

        A nível de implementação, pega todos os valores do
        template e seta nos campos da mensagem.
        """

        def set_campo(field):
            valor = getattr(template, field.name)
            name = field.name

            setattr(self, name, valor)

        template = self.template_email
        fields = template._meta.fields[1:]
        list(map(set_campo, fields))

        destinatarios = self.template_email.destinatarios.all()
        self.destinatarios.set(destinatarios)
        self.save()

    def save(self, *args, **kwargs):
        """Sobrescrita do método save para realizarmos ações personalizadas."""
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        super(MensagemEmail, self).save(*args, **kwargs)

    def enviar(self, objeto=None, destinatarios_extra=[]):
        """Função para enviar o e-mail."""
        if not self.enviado:
            ENVIAR_EMAIL = config("ENVIAR_EMAIL", default=True, cast=bool)
            template_renderizado = Template(
                self.template_email.corpo_email.html
            )
            texto_renderizado = Template(self.template_email.corpo_email.plain)
            assunto_renderizado = Template(self.template_email.assunto)
            context = Context({"objeto": objeto})

            html_text = template_renderizado.render(context)
            assunto_text = assunto_renderizado.render(context)

            text = texto_renderizado.render(context)
            self.corpo_email_text = text

            objeto.id if objeto and objeto.id else ""

            titulo_alteracao = self.template_email.titulo_alteracao_email
            html_email = render_to_string(
                "emails/base.html",
                {
                    "titulo_email": self.template_email.titulo_email,
                    "legenda_email": self.template_email.legenda_email,
                    "titulo_alteracao_email": titulo_alteracao,
                    "html_text": html_text,
                    "objeto": objeto,
                },
            )

            destinatarios = [
                destinatario.email
                for destinatario in self.template_email.destinatarios.all()
            ]
            destinatarios += destinatarios_extra

            try:
                if self.template_email.enviar_usuario_criacao:
                    destinatarios.append(objeto.usuario_criacao.email)
            except Exception:
                pass

            email = EmailMessage(
                assunto_text,
                html_email,
                "{} <{}>".format(
                    settings.EMAIL_NAME, settings.EMAIL_HOST_USER
                ),
                destinatarios,
            )
            email.content_subtype = "html"

            self.save()
            if ENVIAR_EMAIL:
                email.send()
                self.enviado = True
                self.save()

    def __str__(self):
        """Método que retorna a representação do objeto como string."""
        return self.template_email.assunto

    class Meta:
        """Sub classe para definir meta atributos da classe principal."""

        app_label = "emails"
        verbose_name = "Mensagem do email"
        verbose_name_plural = "Mensagens dos emails"
