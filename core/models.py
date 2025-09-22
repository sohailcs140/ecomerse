"""
Core models for the ecommerce application.
"""

from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
    """
    Abstract base class that provides self-updating created_at and updated_at fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Brand(TimestampedModel):
    """
    Brand model for product brands.
    """
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='brands/', blank=True, null=True)
    status = models.BooleanField(default=True)
    is_home = models.BooleanField(default=False, help_text="Show on homepage")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'brands'
        ordering = ['name']


class Category(TimestampedModel):
    """
    Category model with hierarchical support.
    """
    category_name = models.CharField(max_length=100)
    category_slug = models.SlugField(max_length=100, unique=True)
    parent_category = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='subcategories'
    )
    category_image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_home = models.BooleanField(default=False, help_text="Show on homepage")
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'
        ordering = ['category_name']


class Color(TimestampedModel):
    """
    Color model for product variants.
    """
    color = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.color

    class Meta:
        db_table = 'colors'
        ordering = ['color']


class Size(TimestampedModel):
    """
    Size model for product variants.
    """
    size = models.CharField(max_length=20)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.size

    class Meta:
        db_table = 'sizes'
        ordering = ['size']


class Tax(TimestampedModel):
    """
    Tax model for product taxation.
    """
    tax_desc = models.CharField(max_length=100)
    tax_value = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tax_desc} ({self.tax_value}%)"

    class Meta:
        db_table = 'taxs'
        verbose_name_plural = 'taxes'


class Coupon(TimestampedModel):
    """
    Coupon model for discount management.
    """
    COUPON_TYPE_CHOICES = [
        ('Value', 'Fixed Value'),
        ('Per', 'Percentage'),
    ]
    
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=COUPON_TYPE_CHOICES)
    min_order_amt = models.DecimalField(max_digits=10, decimal_places=2)
    is_one_time = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.code})"

    class Meta:
        db_table = 'coupons'


class HomeBanner(TimestampedModel):
    """
    Home page banner model.
    """
    image = models.ImageField(upload_to='banners/')
    btn_txt = models.CharField(max_length=50, blank=True, null=True)
    btn_link = models.URLField(blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Banner {self.id}"

    class Meta:
        db_table = 'home_banners'


class OrderStatus(models.Model):
    """
    Order status model.
    """
    orders_status = models.CharField(max_length=50)

    def __str__(self):
        return self.orders_status

    class Meta:
        db_table = 'orders_status'
        verbose_name_plural = 'order statuses'