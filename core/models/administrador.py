from django.db import models
from .profile import Profile


class Adiministrador(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.SET_NULL,
        verbose_name="Adiministrador",
        null=True
    )

    class Meta:
        app_label = 'core'
        verbose_name = 'Adiministrador'
        verbose_name_plural = 'Adiministradores'