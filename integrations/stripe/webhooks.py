from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from core.models import OrderStatus
from .client import StripeClient
from core.enums import PaymentStatus
stripe_client = StripeClient()

@csrf_exempt
def webhook_view(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    # Check if signature header is present
    if not sig_header:
        print("ERROR: No signature header found in request")
        return HttpResponse(status=400)
    
    # Check if webhook secret is configured
    if not stripe_client.webhook_secret:
        print("ERROR: No webhook secret configured")
        return HttpResponse(status=400)

    try:
        event = stripe_client.construct_event(payload, sig_header)
        print(f"Webhook event constructed successfully: {event['type']}")
    except Exception as e:
        print("Error in webhook_view", e)
        print(f"Error type: {type(e).__name__}")
        print(f"Payload (first 200 chars): {payload[:200]}")
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        order_id = intent["metadata"].get("order_id")

        # Update payment status
        Order.objects.filter(id=order_id).update(
            payment_status=PaymentStatus.SUCCESS.value
        )

    elif event["type"] == "payment_intent.payment_failed":
        intent = event["data"]["object"]
        order_id = intent["metadata"].get("order_id")
        
        # Update payment status
        Order.objects.filter(id=order_id).update(
            payment_status=PaymentStatus.FAILED.value
        )

    return HttpResponse(status=200)