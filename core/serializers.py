"""
Core serializers for the ecommerce application.
"""

from rest_framework import serializers
from .models import Brand, Category, Color, Size, Tax, Coupon, HomeBanner,OrderStatus
from django.db import models
from django.utils import timezone
from django.apps import apps
from orders.models import Order
from django.db.models import Sum

class BrandSerializer(serializers.ModelSerializer):
    """
    Brand serializer.
    """
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer with subcategories support.
    """
    subcategories = serializers.SerializerMethodField()
    parent_category_name = serializers.CharField(source='parent_category.category_name', read_only=True)
    product_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

    def get_subcategories(self, obj):
        if obj.subcategories.exists():
            return CategorySerializer(obj.subcategories.filter(status=True), many=True).data
        return []
    
    def get_product_count(self, obj):
        return obj.product_count


class CategoryKpisSerializer(serializers.Serializer):
    active_categories_count = serializers.SerializerMethodField()
    inactive_categories_count = serializers.SerializerMethodField()
    category_with_products_count = serializers.SerializerMethodField()

    def get_active_categories_count(self, obj):
        return Category.objects.filter(status=True).count()

    def get_inactive_categories_count(self, obj):
        return Category.objects.filter(status=False).count()

    def get_category_with_products_count(self, obj):
        return Category.objects.annotate(product_count=models.Count('products')).filter(product_count__gt=0).count()



class ColorSerializer(serializers.ModelSerializer):
    """
    Color serializer.
    """
    class Meta:
        model = Color
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    """
    Size serializer.
    """
    class Meta:
        model = Size
        fields = '__all__'


class TaxSerializer(serializers.ModelSerializer):
    """
    Tax serializer.
    """
    class Meta:
        model = Tax
        fields = '__all__'


class CouponSerializer(serializers.ModelSerializer):
    """
    Coupon serializer.
    """
    class Meta:
        model = Coupon
        fields = '__all__'


class HomeBannerSerializer(serializers.ModelSerializer):
    """
    Home banner serializer.
    """
    class Meta:
        model = HomeBanner
        fields = '__all__'


class OrderStatusSerializer(serializers.ModelSerializer):
    """
    Order status serializer.
    """
    class Meta:
        model = OrderStatus
        fields = '__all__'


class OrderStatusOverviewSerializer(serializers.Serializer):
    """
    Order status overview serializer.
    """
    order_status = serializers.SerializerMethodField()
    order_status_count = serializers.SerializerMethodField()
    def get_order_status(self, obj):
        return obj.orders_status

    def get_order_status_count(self, obj):
        return Order.objects.filter(order_status=obj).count()



class DashboardKPISerializer(serializers.Serializer):
    """
    Dashboard KPI serializer.
    """
    total_products_count = serializers.SerializerMethodField()
    total_orders_count = serializers.SerializerMethodField()
    total_revenue = serializers.SerializerMethodField()
    low_stock_alert_count = serializers.SerializerMethodField()
    last_month_revenue = serializers.SerializerMethodField()
    this_month_revenue = serializers.SerializerMethodField()
    revenue_growth = serializers.SerializerMethodField()
    recent_orders = serializers.SerializerMethodField()
    order_status_overview = serializers.SerializerMethodField()
    low_stock_products = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Product = apps.get_model('products', 'Product')
        self.Order = apps.get_model('orders', 'Order')
        self.OrderStatus = apps.get_model('core', 'OrderStatus')
        from products.serializers import ProductDetailSerializer
        self.ProductDetailSerializer = ProductDetailSerializer

    # --- Product KPIs ---
    def get_low_stock_products(self, obj):
        """Return list of products whose total stock (sum of all attributes) is below 10."""
        # from products.serializers import ProductSerializer
        low_stock_products = (
            self.Product.objects
            .annotate(total_qty=models.Sum('attributes__qty'))
            .filter(total_qty__lt=5)
        )
        return self.ProductDetailSerializer(low_stock_products, many=True).data

    def get_low_stock_alert_count(self, obj):
        """Count how many products have low stock."""
        return (
            self.Product.objects
            .annotate(total_qty=models.Sum('attributes__qty'))
            .filter(total_qty__lt=5)
            .count()
        )

    def get_total_products_count(self, obj):
        return self.Product.objects.count()

    # --- Order KPIs ---
    def get_recent_orders(self, obj):
        from orders.serializers import OrderSerializer
        return OrderSerializer(
            self.Order.objects.order_by('-added_on')[:10], many=True
        ).data

    def get_total_orders_count(self, obj):
        return self.Order.objects.count()

    def get_total_revenue(self, obj):
        return (
            self.Order.objects.aggregate(total_revenue=models.Sum('total_amt'))
            .get('total_revenue') or 0
        )

    # --- Revenue KPIs ---
    def get_last_month_revenue(self, obj):
        now = timezone.now()
        last_month = now.month - 1 or 12
        year = now.year if now.month > 1 else now.year - 1
        return (
            self.Order.objects.filter(added_on__year=year, added_on__month=last_month)
            .aggregate(total_revenue=models.Sum('total_amt'))
            .get('total_revenue') or 0
        )

    def get_this_month_revenue(self, obj):
        now = timezone.now()
        return (
            self.Order.objects.filter(added_on__year=now.year, added_on__month=now.month)
            .aggregate(total_revenue=models.Sum('total_amt'))
            .get('total_revenue') or 0
        )

    def get_revenue_growth(self, obj):
        last = self.get_last_month_revenue(obj)
        this = self.get_this_month_revenue(obj)

        if last == 0 and this > 0:
            return 100.0
        elif last == 0 and this == 0:
            return 0.0
        return ((this - last) / last) * 100

    # --- Order Status Overview ---
    def get_order_status_overview(self, obj):
        from .serializers import OrderStatusOverviewSerializer
        return OrderStatusOverviewSerializer(self.OrderStatus.objects.all(), many=True).data