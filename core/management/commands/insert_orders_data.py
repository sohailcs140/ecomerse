"""
Django management command to insert demo orders and users.
Creates at least 10 users and 10 orders per user with realistic details.
Run: python manage.py insert_orders_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from decimal import Decimal
import random
import string

from core.models import OrderStatus, Coupon
from products.models import ProductAttribute
from orders.models import Order, OrderDetail

User = get_user_model()


def random_phone():
    return "03" + "".join(random.choices("0123456789", k=9))


def random_address():
    streets = ["Mall Road", "Ferozepur Road", "University Ave", "Johar Town", "Model Town"]
    cities = ["Lahore", "Karachi", "Islamabad", "Rawalpindi", "Faisalabad"]
    states = ["Punjab", "Sindh", "Islamabad Capital Territory", "Punjab", "Punjab"]
    idx = random.randrange(len(streets))
    return (
        f"House {random.randint(10, 999)}, {streets[idx]}|{cities[idx]}|{states[idx]}|{random.randint(54000, 79999)}"
    )


class Command(BaseCommand):
    help = "Insert at least 10 users and 10 orders per user using existing products"

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=10, help="Minimum number of users to seed")
        parser.add_argument("--orders", type=int, default=10, help="Orders per user to create")

    def handle(self, *args, **options):
        min_users = max(10, options["users"])
        orders_per_user = max(10, options["orders"])

        # Preconditions
        product_attrs = list(ProductAttribute.objects.select_related("product").all())
        if not product_attrs:
            self.stdout.write(self.style.ERROR("No product attributes found. Seed products first."))
            return

        order_statuses = list(OrderStatus.objects.all())
        if not order_statuses:
            self.stdout.write(self.style.ERROR("No order statuses found. Seed core data first."))
            return

        coupons = list(Coupon.objects.all())

        # Ensure minimum users
        self.stdout.write(f"Ensuring at least {min_users} users...")
        existing_users = list(User.objects.all())
        users_needed = max(0, min_users - len(existing_users))

        created_users = []
        for i in range(users_needed):
            username = f"demo_user_{len(existing_users) + i + 1}"
            email = f"{username}@example.com"
            user = User.objects.create_user(
                username=username,
                email=email,
                password="Password123!",
                first_name=f"Demo{len(existing_users) + i + 1}",
                last_name="User",
            )
            created_users.append(user)
        users = list(User.objects.all())
        self.stdout.write(self.style.SUCCESS(f"Users total: {len(users)} (created {len(created_users)})"))

        # Create orders per user
        total_orders_created = 0
        for user in users[:min_users]:
            for _ in range(orders_per_user):
                with transaction.atomic():
                    # Choose random 1-3 items
                    items = random.sample(product_attrs, k=min(len(product_attrs), random.randint(1, 3)))

                    # Build address parts
                    address_line, city, state, pincode = random_address().split("|")

                    # Status and payment
                    status = random.choice(order_statuses)
                    payment_type = random.choice(["COD", "Gateway"])
                    payment_status = random.choice(["Pending", "Success", "Failed"]) if payment_type == "Gateway" else "Pending"

                    # Create order shell
                    order = Order.objects.create(
                        user=user,
                        name=f"{user.first_name} {user.last_name}".strip() or user.email,
                        email=user.email or f"{user.email}",
                        mobile=random_phone(),
                        address=address_line,
                        city=city,
                        state=state,
                        pincode=pincode,
                        coupon_code=None,
                        coupon_value=Decimal("0.00"),
                        order_status=status,
                        payment_type=payment_type,
                        payment_status=payment_status,
                        payment_id=("PAY_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))) if payment_type == "Gateway" else None,
                        txn_id=("TXN_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))) if payment_type == "Gateway" else None,
                        total_amt=Decimal("0.00"),
                        track_details="",
                    )

                    # Add items
                    subtotal = Decimal("0.00")
                    for attr in items:
                        qty = random.randint(1, 3)
                        OrderDetail.objects.create(
                            order=order,
                            product=attr.product,
                            product_attr=attr,
                            price=attr.price,
                            qty=qty,
                        )
                        subtotal += (attr.price * qty)

                    # Maybe apply a coupon (20% chance)
                    applied_coupon_code = None
                    applied_coupon_value = Decimal("0.00")
                    if coupons and random.random() < 0.2:
                        c = random.choice(coupons)
                        if c.type == "Value":
                            applied_coupon_value = Decimal(c.value)
                        else:
                            applied_coupon_value = (subtotal * Decimal(c.value) / Decimal("100"))
                        applied_coupon_code = c.code

                    # Total (no shipping/tax calc here; keep simple)
                    total = subtotal - applied_coupon_value
                    if total < 0:
                        total = Decimal("0.00")

                    # Save totals/coupon
                    order.coupon_code = applied_coupon_code
                    order.coupon_value = applied_coupon_value
                    order.total_amt = total
                    order.save()

                    total_orders_created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Inserted {total_orders_created} orders across {min_users} users (>= {orders_per_user} each)."
        ))
        self.stdout.write(self.style.SUCCESS("Done."))
