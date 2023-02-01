from djoser import email
from decouple import config

class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'registration/email/password_reset.html'

    def get_context_data(self):
        # PasswordResetEmail can be deleted
        context = super().get_context_data()
        context['domain'] = config('DOMAIN_FRONT', default=context['domain'])
        context['site_name'] = "VPS"
        return context