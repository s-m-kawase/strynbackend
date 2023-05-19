import stripe
import os


class StripeCheckoutSession:
    def __init__(self):
        # Recupere a chave secreta do ambiente
        stripe_secret_key = os.environ.get('STRIPE_SECRET_KEY')

        # Configure a chave secreta do Stripe
        stripe.api_key = stripe_secret_key

    def create_session(self, line_items, payment_method_types, success_url, cancel_url):
        session = stripe.checkout.Session.create(
            payment_method_types=payment_method_types,
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )

        return session.id
