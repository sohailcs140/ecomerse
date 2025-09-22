"""
Customer models for the ecommerce application.
"""

from django.db import models
from django.conf import settings
from core.models import TimestampedModel


class Customer(TimestampedModel):
    """
    Customer profile model with one-to-one relationship to User.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    gstin = models.CharField(max_length=20, blank=True, null=True)
    status = models.BooleanField(default=True)
    is_verify = models.BooleanField(default=False)
    is_forgot_password = models.BooleanField(default=False)
    rand_id = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"

    class Meta:
        db_table = 'customers'
        ordering = ['-created_at']

    @property
    def email(self):
        """Get email from related user."""
        return self.user.email

    @property
    def is_active(self):
        """Get active status from related user."""
        return self.user.is_active