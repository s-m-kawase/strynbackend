from django.contrib import admin
from emails.models import ConfiguracaoEmail
from novadata_utils.admin import NovadataModelAdmin


@admin.register(ConfiguracaoEmail)
class ConfiguracaoEmailAdmin(NovadataModelAdmin):
    ...
