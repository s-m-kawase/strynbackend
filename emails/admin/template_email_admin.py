from django.contrib import admin

from ..models import TemplateEmail


@admin.register(TemplateEmail)
class TemplateEmailAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'assunto',
        'codigo'
    ]

    search_fields = [
        'id',
        'assunto',
        'codigo'
    ]

    filter_horizontal = [
        'destinatarios'
    ]

    exclude = [
        'legenda_email',
        'titulo_alteracao_email'
    ]
