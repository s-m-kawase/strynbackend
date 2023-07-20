from django.apps import AppConfig


class EmailsConfig(AppConfig):
    name = "emails"

    def ready(self):
        import emails.signals

        try:
            from emails.models import ConfiguracaoEmail
            from emails.signals.configuracao_email_signals import (
                setar_variaveis_email,
            )

            configuracao_email = ConfiguracaoEmail.objects.first()
            if not configuracao_email:
                configuracao_email = ConfiguracaoEmail.objects.create()
            setar_variaveis_email(configuracao_email)
        except Exception:
            pass
