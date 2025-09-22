"""
Order models for the ecommerce application.
"""

from django.db import models
from django.conf import settings
from core.models import OrderStatus
from products.models import Product, ProductAttribute


class Order(models.Model):
    """
    Order model.
    """
    PAYMENT_TYPE_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Gateway', 'Payment Gateway'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    ]

    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    coupon_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    txn_id = models.CharField(max_length=100, blank=True, null=True)
    total_amt = models.DecimalField(max_digits=10, decimal_places=2)
    track_details = models.TextField(blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.name}"

    class Meta:
        db_table = 'orders'
        ordering = ['-added_on']


class OrderDetail(models.Model):
    """
    Order details model for individual items in an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_attr = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveIntegerField()

    def __str__(self):
        return f"Order #{self.order.id} - {self.product.name}"

    class Meta:
        db_table = 'orders_details'


class Cart(models.Model):
    """
    Shopping cart model.
    """
    USER_TYPE_CHOICES = [
        ('Reg', 'Registered'),
        ('Not-Reg', 'Not Registered'),
    ]

    user_id = models.CharField(max_length=20)  # Can be customer ID or session ID
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    qty = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_attr = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.user_id} - {self.product.name}"

    class Meta:
        db_table = 'cart'