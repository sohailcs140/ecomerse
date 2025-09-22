"""
Customer admin configuration.
"""

from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_email', 'get_username', 'mobile', 'status', 'is_verify', 'created_at']
    list_filter = ['status', 'is_verify', 'user__user_type', 'created_at']
    search_fields = ['name', 'user__email', 'user__username', 'mobile']
    readonly_fields = ['user', 'created_at', 'updated_at']
    
    def get_email(self, obj):
        """Get email from related user."""
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'
    
    def get_username(self, obj):
        """Get username from related user."""
        return obj.user.username
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'