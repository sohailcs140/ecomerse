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
        # Use email as default name since username can be null
        default_name = instance.username or instance.email.split('@')[0]
        Customer.objects.create(
            user=instance,
            name=default_name,
            mobile=getattr(instance, 'mobile', '') or ''
        )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_customer_profile(sender, instance, **kwargs):
    """
    Save the customer profile when the user is saved.
    """
    if instance.user_type == 'customer' and hasattr(instance, 'customer_profile'):
        instance.customer_profile.save()
