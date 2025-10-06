"""
Order admin configuration.
"""

from django.contrib import admin
from .models import Order, OrderDetail, Cart


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 0
    readonly_fields = ['product', 'product_attr', 'price', 'qty']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'email', 'order_status', 'payment_type', 'payment_status', 'total_amt', 'added_on']
    list_filter = ['order_status', 'payment_type', 'payment_status', 'added_on']
    search_fields = ['name', 'email', 'mobile']
    readonly_fields = ['added_on']
    inlines = [OrderDetailInline]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'user_type', 'product', 'qty', 'added_on']
    list_filter = ['user_type', 'added_on']
    search_fields = ['user_id', 'product__name']