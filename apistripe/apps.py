from django.apps import AppConfig

class ApistripeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apistripe'

    def ready(self):
        import apistripe.signals
