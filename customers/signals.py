"""
Customer signals for automatic profile creation.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Customer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_profile(sender, instance, created, **kwargs):
    """
    Create a customer profile when a new user with user_type='customer' is created.
    """
    if created and instance.user_type == 'customer':
        Customer.objects.create(
            user=instance,
            name=instance.username,  # Default name to username
            mobile=getattr(instance, 'mobile', '') or ''
        )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_customer_profile(sender, instance, **kwargs):
    """
    Save the customer profile when the user is saved.
    """
    if instance.user_type == 'customer' and hasattr(instance, 'customer_profile'):
        instance.customer_profile.save()
