from .configuracao_email_signals import configuracao_email_post_save
from .mensagem_email_signals import mensagem_email_post_save

__all__ = [
    configuracao_email_post_save,
    mensagem_email_post_save,
]
