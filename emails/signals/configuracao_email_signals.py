from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import ConfiguracaoEmail


@receiver(post_save, sender=ConfiguracaoEmail)
def configuracao_email_post_save(sender, instance, created, **kwargs):
    """Realiza ações após a model ConfiguracaoEmail ser salva."""
    setar_variaveis_email(instance)


def setar_variaveis_email(config_email):
    """Seta as variáveis para o envio de e-mail no settings."""
    from django.conf import settings

    setattr(settings, "EMAIL_BACKEND", config_email.email_backend)
    setattr(settings, "EMAIL_USE_TLS", config_email.email_use_tls)
    setattr(settings, "EMAIL_HOST", config_email.email_host)
    setattr(settings, "EMAIL_PORT", config_email.email_port)
    setattr(settings, "EMAIL_HOST_USER", config_email.email_host_user)
    setattr(settings, "EMAIL_HOST_PASSWORD", config_email.email_host_password)
    setattr(settings, "DEFAULT_FROM_EMAIL", config_email.default_from_email)
    setattr(settings, "EMAIL_NAME", config_email.email_name)
