from django.apps import AppConfig


class EmailsConfig(AppConfig):
    name = 'emails'

    def ready(self):
        from . import signals