"""
Order serializers for the ecommerce application.
"""

from rest_framework import serializers
from .models import Order, OrderDetail, Cart
from products.serializers import ProductListSerializer, ProductAttributeSerializer


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Order detail serializer.
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.CharField(source='product.image.url', read_only=True)
    product_attr = ProductAttributeSerializer(read_only=True)

    class Meta:
        model = OrderDetail
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """
    Order serializer.
    """
    order_details = OrderDetailSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    order_status_name = serializers.CharField(source='order_status.orders_status', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['customer', 'added_on']


class CartSerializer(serializers.ModelSerializer):
    """
    Cart serializer.
    """
    product = ProductListSerializer(read_only=True)
    product_attr = ProductAttributeSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_total_price(self, obj):
        return obj.product_attr.price * obj.qty


class CartAddSerializer(serializers.ModelSerializer):
    """
    Cart add serializer for adding items to cart.
    """
    class Meta:
        model = Cart
        fields = ['user_id', 'user_type', 'qty', 'product', 'product_attr']
