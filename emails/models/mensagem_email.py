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
from .template_email import TemplateEmail
from crum import get_current_user
from django.template.loader import render_to_string
from decouple import config
from django.core.mail import EmailMessage
from .destinatario import Destinatario
from django.template.loader import get_template
from django.template import Context, Template



class MensagemEmail(models.Model):
    """
    Classe que serve de fato para enviar os emails
    """
    template_email = models.ForeignKey(
        TemplateEmail,
        verbose_name = "Template do email",
        on_delete = models.CASCADE
    )


    enviado = models.BooleanField(
        verbose_name = "Enviado",
        default = False
    )


    data_criacao = models.DateTimeField(
        auto_now_add = True,
        verbose_name = "Data de criação"
    )


    created_by = models.ForeignKey(
		'auth.User', 
		related_name='%(class)s_requests_created',
		blank=True,
        null=True,
		default=None,
		on_delete=models.SET_NULL
	)


    def save(self, *args, **kwargs):
        user = get_current_user()
        criacao = False
        if user and not user.pk:
            user = None
        if not self.pk:
            self.usuario_criacao = user
            criacao = True
        super(MensagemEmail, self).save(*args, **kwargs)


    def enviar(self, objeto=None, destinatarios_extra=[]):
        if not self.enviado:
            ENVIAR_EMAIL = config('ENVIAR_EMAIL', default = True, cast = bool)
            template_renderizado = Template(self.template_email.corpo_email)
            assunto_renderizado = Template(self.template_email.assunto)
            context = Context(
                { "objeto":  objeto}
            )

            html_text = template_renderizado.render(context)
            assunto_text = assunto_renderizado.render(context)
            nome = objeto.__str__ if objeto.__str__ else ''
            if nome and type(nome) == str:
                nome = nome.replace(' ', '-')
            id = objeto.id if objeto.id else ''

            html_email = render_to_string(
                'emails/base.html',
                {
                    'titulo_email': self.template_email.titulo_email,
                    'legenda_email': self.template_email.legenda_email,
                    'titulo_alteracao_email': self.template_email.titulo_alteracao_email,
                    'html_text': html_text,
                    'nome': nome,
                    'id': id
                }
            )
            
            destinatarios = [destinatario.email for destinatario in self.template_email.destinatarios.all()]
            destinatarios += destinatarios_extra
            
            try:
                if self.template_email.enviar_usuario_criacao:
                    destinatarios.append(objeto.usuario_criacao.email)
            except:
                pass
                
            email = EmailMessage(
                assunto_text, html_email,
                '{} <{}>'.format(config('EMAIL_NAME'), config('EMAIL_HOST_USER')), destinatarios)
            email.content_subtype = "html"

            if ENVIAR_EMAIL:
                email.send()
                self.enviado = True
                self.save()


    def __str__(self):
        return self.template_email.assunto

        
    class Meta:
        app_label = "emails"
        verbose_name = "Mensagem do email"
        verbose_name_plural = "Mensagens dos emails"