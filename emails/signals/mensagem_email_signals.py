from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import MensagemEmail


@receiver(post_save, sender=MensagemEmail)
def mensagem_email_post_save(sender, instance, created, **kwargs):
    """Realiza ações após a model MensagemEmail ser salva."""
    if created:
        instance.gerar_historico()
