"""
Core serializers for the ecommerce application.
"""

from rest_framework import serializers
from .models import Brand, Category, Color, Size, Tax, Coupon, HomeBanner, OrderStatus
from django.db import models

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
