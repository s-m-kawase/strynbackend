from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from ..models import Cupom
from django.utils import timezone


@receiver(pre_save, sender=Cupom)
def marcar_expirado_cupom(sender, instance, **kwargs):
    if instance.validado_ate and instance.validado_ate < timezone.now():
        instance.marcar_expirado()


@receiver(post_save, sender=Cupom)
def marcar_valido_cupom(sender, instance, **kwargs):
    if instance.validado_ate and instance.validado_ate < timezone.now():
        instance.marcar_expirado()