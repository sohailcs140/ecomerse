import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_api.settings')
django.setup()

from core.models import Brand, Category, Color, Size, Tax
from products.models import Product, ProductAttribute
from decimal import Decimal
import time
import random

def generate_unique_slug(product_name):
    base_slug = f"{product_name.lower().replace(' ', '-').replace(',', '').replace('(', '').replace(')', '')}"
    unique_slug = f"{base_slug}-{int(time.time())}-{random.randint(1000, 9999)}"
    
    counter = 1
    original_slug = unique_slug
    while Product.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{original_slug}-{counter}"
        counter += 1
    
    return unique_slug

# Get existing data
brand = Brand.objects.get(name='WoodCraft Pro')
category = Category.objects.get(category_slug='book-holders')
color1 = Color.objects.get(color='#D2B48C')
size_small = Size.objects.get(size='Small')
tax = Tax.objects.first()

# Create test product
product_name = 'Test Wooden Book Holder - Premium Quality'
unique_slug = generate_unique_slug(product_name)
print(f'Generated slug: {unique_slug}')

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
    print(f'✅ Created product: {product.name}')
    print(f'✅ Slug: {product.slug}')
    
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
    print('✅ Created product attribute')
else:
    print(f'Product already exists: {product.name}')
