from django.contrib import admin
from novadata_utils.admin import NovadataModelAdmin

from ..models import MensagemEmail


@admin.register(MensagemEmail)
class MensagemEmailAdmin(NovadataModelAdmin):
    def has_add_permission(self, request):
        """Informa se o usuário pode adicionar uma mensagem de email."""
        return False

    list_filter = [
        "template_email",
        "enviado",
        "created_by",
        "data_criacao",
        "codigo",
        "enviar_usuario_criacao",
    ]

    search_fields = [
        "id",
        "template_email__assunto",
        "created_by__first_name",
        "created_by__last_name",
    ]

    readonly_fields = [
        "template_email",
        "enviado",
        "created_by",
        #
        "assunto",
        "titulo_email",
        "legenda_email",
        "titulo_alteracao_email",
        "corpo_email",
        "corpo_email_text",
        "codigo",
        "enviar_usuario_criacao",
        "destinatarios",
    ]

    fieldsets = [
        (
            "Dados da mensagem",
            {
                "fields": [
                    "template_email",
                    "enviado",
                    "created_by",
                ]
            },
        ),
        (
            "Dados do template",
            {
                "fields": [
                    "assunto",
                    "titulo_email",
                    "legenda_email",
                    "titulo_alteracao_email",
                    "corpo_email",
                    "corpo_email_text",
                    "codigo",
                    "enviar_usuario_criacao",
                    "destinatarios",
                ]
            },
        ),
    ]
