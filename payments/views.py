from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
from core.models import OrderStatus
from integrations.stripe.client import StripeClient
from django.contrib.auth import get_user_model
from products.models import Product, ProductAttribute
from orders.models import OrderDetail, Cart
from core.enums import PaymentStatus, PaymentType

User = get_user_model()
stripe_client = StripeClient()

@api_view(["POST"])
def create_payment_intent(request):
    try:
        # Extract data from request
        amount = int(request.data.get("amount"))
        currency = request.data.get("currency", "pkr")
        order_data = request.data.get("order_data", {})
        
        # Get contact info and shipping address
        contact_info = order_data.get("contact_info", {})
        shipping_address = order_data.get("shipping_address", {})
        
        # Get or create pending order status
        order_status = OrderStatus.objects.filter(is_default=True).first()

        
        # Create order with all required fields and convert from paisa to rupees
        order = Order.objects.create(
            user=request.user,
            name=f"{contact_info.get('firstName', '')} {contact_info.get('lastName', '')}".strip(),
            email=contact_info.get("emailAddress", ""),
            mobile=contact_info.get("phoneNumber", ""),
            address=shipping_address.get("streetAddress", ""),
            city=shipping_address.get("townCity", ""),
            state=shipping_address.get("state", ""),
            pincode=shipping_address.get("zipCode", ""),
            coupon_code=order_data.get("coupon_code"),
            coupon_value=order_data.get("discount", 0),
            order_status=order_status,
            payment_type=PaymentType.GATEWAY.value,
            payment_status=PaymentStatus.PENDING.value,
            total_amt=amount / 100,  # Convert from paisa to rupees
        )

        # Create Stripe payment intent
        intent = stripe_client.create_payment_intent(
            amount=amount,
            currency=currency,
            metadata={
                "order_id": order.id,
                "user_id": str(request.user.id),
                "email": contact_info.get("emailAddress", ""),
            },
        )

        order.payment_id = intent.id
        order.save()

        cart_items = order_data.get("cart_items", [])
        for item in cart_items:
            try:
                product = Product.objects.get(id=item.get("product_id").get("id"))
                product_attr = ProductAttribute.objects.get(id=item.get("product_attr_id"))
                
                OrderDetail.objects.create(
                    order=order,
                    product=product,
                    product_attr=product_attr,
                    price=item.get("price", 0),
                    qty=item.get("quantity", 1),
                )
            except (Product.DoesNotExist, ProductAttribute.DoesNotExist) as e:
                print(f"Error creating order detail for item {item}: {e}")
                continue
        
        Cart.objects.filter(user_id=request.user.id).delete()
        
        return Response({
            "client_secret": intent.client_secret,
            "order_id": order.id,
            "payment_intent_id": intent.id
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

