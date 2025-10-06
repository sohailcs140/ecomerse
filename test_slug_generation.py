#!/usr/bin/env python
"""
Test script for improved slug generation.
"""

import os
import sys
import django
from django.conf import settings

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_api.settings')

# Setup Django
django.setup()

from core.models import Brand, Category, Color, Size, Tax
from products.models import Product, ProductAttribute
from decimal import Decimal
import time
import random

def generate_unique_slug(product_name):
    """Generate a unique slug for a product."""
    base_slug = f"{product_name.lower().replace(' ', '-').replace(',', '').replace('(', '').replace(')', '')}"
    # Add timestamp and random number for uniqueness
    unique_slug = f"{base_slug}-{int(time.time())}-{random.randint(1000, 9999)}"
    
    # Ensure slug is unique
    counter = 1
    original_slug = unique_slug
    while Product.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{original_slug}-{counter}"
        counter += 1
    
    return unique_slug

def create_test_product():
    """Create a test product with improved slug generation."""
    print("Creating test product with improved slug generation...")
    
    try:
        # Get existing data
        brand = Brand.objects.get(name='WoodCraft Pro')
        category = Category.objects.get(category_slug='book-holders')
        color1 = Color.objects.get(color='#D2B48C')  # Natural Wood
        size_small = Size.objects.get(size='Small')
        tax = Tax.objects.first()
        
        # Create product name
        product_name = 'Test Wooden Book Holder - Premium Quality'
        
        # Generate unique slug
        unique_slug = generate_unique_slug(product_name)
        print(f"Generated slug: {unique_slug}")
        
        # Create product
        product, created = Product.objects.get_or_create(
            name=product_name,
            defaults={
                'category': category,
                'brand': brand,
                'model': 'TEST-001',
                'slug': unique_slug,
                'short_desc': 'Test handcrafted wooden book holder.',
                'desc': 'Test product for slug generation.',
                'keywords': 'test, book holder, wooden',
                'technical_specification': 'Test specifications',
                'uses': 'Testing',
                'warranty': '1 year',
                'lead_time': '1 day',
                'tax': tax,
                'is_promo': False,
                'is_featured': False,
                'is_discounted': False,
                'is_arrival': False,
                'status': True
            }
        )
        
        if created:
            print(f"✅ Created product: {product.name}")
            print(f"✅ Slug: {product.slug}")
            
            # Create product attribute
            ProductAttribute.objects.create(
                product=product,
                sku='TEST-001-D2B-S',
                mrp=Decimal('1000.00'),
                price=Decimal('800.00'),
                qty=10,
                size=size_small,
                color=color1
            )
            print("✅ Created product attribute")
        else:
            print(f"Product already exists: {product.name}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    create_test_product()
