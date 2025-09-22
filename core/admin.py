"""
Core admin configuration.
"""

from django.contrib import admin
from .models import Brand, Category, Color, Size, Tax, Coupon, HomeBanner, OrderStatus


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'is_home', 'created_at']
    list_filter = ['status', 'is_home']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'parent_category', 'status', 'is_home', 'created_at']
    list_filter = ['status', 'is_home', 'parent_category']
    search_fields = ['category_name']
    prepopulated_fields = {'category_slug': ('category_name',)}


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['color', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['color']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['size']


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['tax_desc', 'tax_value', 'status', 'created_at']
    list_filter = ['status']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['title', 'code', 'value', 'type', 'min_order_amt', 'status', 'created_at']
    list_filter = ['type', 'status', 'is_one_time']
    search_fields = ['title', 'code']


@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'btn_txt', 'status', 'created_at']
    list_filter = ['status']


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'orders_status']