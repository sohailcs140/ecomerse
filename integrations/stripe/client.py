import stripe
from django.conf import settings


class StripeClient:
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    def create_payment_intent(self, amount, currency="pkr", metadata=None):
        """
        amount must be in the smallest currency unit (paisa for PKR).
        Example: 100 PKR => 10000 paisa
        """
        return stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            metadata=metadata or {},
        )

    def retrieve_payment_intent(self, intent_id):
        return stripe.PaymentIntent.retrieve(intent_id)

    def construct_event(self, payload, sig_header):
        return stripe.Webhook.construct_event(
            payload, sig_header, self.webhook_secret
        )
