"""
Product models for the ecommerce application.
"""

from django.db import models
from django.utils.text import slugify
from core.models import TimestampedModel, Brand, Category, Color, Size, Tax


class Product(TimestampedModel):
    """
    Main product model.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/')
    slug = models.SlugField(max_length=200, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    model = models.CharField(max_length=200, null=True, blank=True)
    short_desc = models.TextField(null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    technical_specification = models.TextField(null=True, blank=True)
    uses = models.CharField(max_length=200, blank=True, null=True)
    warranty = models.CharField(max_length=200, blank=True, null=True)
    lead_time = models.CharField(max_length=100, blank=True, null=True)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, null=True, blank=True)
    is_promo = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_discounted = models.BooleanField(default=False)
    is_arrival = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']


class ProductAttribute(models.Model):
    """
    Product attributes model for variants (size, color, price, etc.).
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    sku = models.CharField(max_length=50, unique=True)
    attr_image = models.ImageField(upload_to='products/attributes/', blank=True, null=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveIntegerField()
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.sku}"

    class Meta:
        db_table = 'products_attr'
        verbose_name = 'Product Attribute'
        verbose_name_plural = 'Product Attributes'


class ProductImage(models.Model):
    """
    Additional product images.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"

    class Meta:
        db_table = 'product_images'


class ProductReview(models.Model):
    """
    Product review model.
    """
    RATING_CHOICES = [
        ('Poor', 'Poor'),
        ('Average', 'Average'),
        ('Good', 'Good'),
        ('Very Good', 'Very Good'),
        ('Excellent', 'Excellent'),
        ('Fantastic', 'Fantastic'),
    ]

    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.CharField(max_length=20, choices=RATING_CHOICES)
    review = models.TextField()
    status = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating}"

    class Meta:
        db_table = 'product_review'