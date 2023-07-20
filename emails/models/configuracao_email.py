from django.db import models
from novadata_utils.models import NovadataModel


class ConfiguracaoEmail(NovadataModel):
    email_backend = models.CharField(
        verbose_name="EMAIL_BACKEND",
        max_length=100,
        default="django.core.mail.backends.smtp.EmailBackend",
    )

    email_use_tls = models.BooleanField(
        verbose_name="EMAIL_USE_TLS",
        default=True,
    )

    email_host = models.CharField(
        verbose_name="EMAIL_HOST",
        max_length=100,
        default="smtp.gmail.com",
    )

    email_port = models.IntegerField(
        verbose_name="EMAIL_PORT",
        default=587,
    )

    email_host_user = models.CharField(
        verbose_name="EMAIL_HOST_USER",
        max_length=100,
        default="hub@novadata.com.br",
    )

    email_host_password = models.CharField(
        verbose_name="EMAIL_HOST_PASSWORD",
        max_length=100,
        default="senhadohub",
    )

    default_from_email = models.CharField(
        verbose_name="DEFAULT_FROM_EMAIL",
        max_length=100,
        default="Novadata <novadata@novadata.com.br>",
    )

    email_name = models.CharField(
        verbose_name="EMAIL_NAME",
        max_length=100,
        default="Novadata",
    )

    def __str__(self):
        """Método que retorna a representação do objeto como string."""
        return "Configuração de e-mail"

    class Meta:
        """Sub classe para definir meta atributos da classe principal."""

        app_label = "emails"
        verbose_name = "Configuração de e-mail"
        verbose_name_plural = "Configurações de e-mail"
