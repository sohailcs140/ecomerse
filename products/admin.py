"""
Product admin configuration.
"""

from django.contrib import admin
from .models import Product, ProductAttribute, ProductImage, ProductReview


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'status', 'is_featured', 'is_promo', 'created_at']
    list_filter = ['status', 'is_featured', 'is_promo', 'is_discounted', 'is_arrival', 'category', 'brand']
    search_fields = ['name', 'keywords']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductAttributeInline, ProductImageInline]


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['product', 'sku', 'size', 'color', 'price', 'qty']
    list_filter = ['size', 'color']
    search_fields = ['sku', 'product__name']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'rating', 'status', 'added_on']
    list_filter = ['rating', 'status']
    search_fields = ['product__name', 'customer__name']