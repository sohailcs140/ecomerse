#!/usr/bin/env python
"""
Simple data insertion script that works around Django URL configuration issues.
"""

import os
import sys
import django
from django.conf import settings

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_api.settings')

# Temporarily disable problematic URL patterns
import django.urls
original_include = django.urls.include

def safe_include(urlconf_module):
    """Safe include that handles missing modules."""
    try:
        return original_include(urlconf_module)
    except ImportError as e:
        print(f"⚠️ Skipping URL pattern due to missing dependency: {e}")
        return []

# Monkey patch the include function
django.urls.include = safe_include

# Setup Django
django.setup()

from core.models import Brand, Category, Color, Size, Tax, Coupon, OrderStatus
from products.models import Product, ProductAttribute, ProductImage
from decimal import Decimal
import time
import random

def generate_unique_slug(product_name):
    """Generate a unique slug for a product."""
    base_slug = f"{product_name.lower().replace(' ', '-').replace(',', '').replace('(', '').replace(')', '')}"
    unique_slug = f"{base_slug}-{int(time.time())}-{random.randint(1000, 9999)}"
    
    counter = 1
    original_slug = unique_slug
    while Product.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{original_slug}-{counter}"
        counter += 1
    
    return unique_slug

def insert_all_data():
    """Insert all data into the database."""
    print("🚀 Starting comprehensive data insertion...")
    
    # Step 1: Create Brands
    print("📦 Creating brands...")
    brands_data = [
        {'name': 'WoodCraft Pro', 'status': True, 'is_home': True},
        {'name': 'Artisan Wood', 'status': True, 'is_home': True},
        {'name': 'Premium Woodworks', 'status': True, 'is_home': False},
        {'name': 'Handmade Heritage', 'status': True, 'is_home': True},
        {'name': 'EcoWood Solutions', 'status': True, 'is_home': True},
        {'name': 'Master Craftsmen', 'status': True, 'is_home': False},
    ]
    
    for brand_data in brands_data:
        brand, created = Brand.objects.get_or_create(
            name=brand_data['name'],
            defaults=brand_data
        )
        if created:
            print(f"  ✅ Created brand: {brand.name}")
    
    # Step 2: Create Colors with hex values
    print("🎨 Creating colors with hex values...")
    colors_data = [
        {'color': '#D2B48C', 'status': True},  # Natural Wood (Tan)
        {'color': '#8B4513', 'status': True},  # Walnut (Saddle Brown)
        {'color': '#DEB887', 'status': True},  # Oak (Burlywood)
        {'color': '#A0522D', 'status': True},  # Cherry (Sienna)
        {'color': '#800000', 'status': True},  # Mahogany (Maroon)
        {'color': '#F5DEB3', 'status': True},  # Pine (Wheat)
        {'color': '#9ACD32', 'status': True},  # Bamboo (Yellow Green)
        {'color': '#F4A460', 'status': True},  # Beech (Sandy Brown)
        {'color': '#CD853F', 'status': True},  # Teak (Peru)
        {'color': '#8B7355', 'status': True},  # Dark Wood (Dark Khaki)
        {'color': '#2F4F4F', 'status': True},  # Dark Slate Gray
        {'color': '#D2691E', 'status': True},  # Chocolate
    ]
    
    for color_data in colors_data:
        color, created = Color.objects.get_or_create(
            color=color_data['color'],
            defaults=color_data
        )
        if created:
            print(f"  ✅ Created color: {color.color}")
    
    # Step 3: Create Sizes
    print("📏 Creating sizes...")
    sizes_data = [
        {'size': 'Small', 'status': True},
        {'size': 'Medium', 'status': True},
        {'size': 'Large', 'status': True},
        {'size': 'Extra Large', 'status': True},
        {'size': 'One Size', 'status': True},
        {'size': 'Custom', 'status': True},
    ]
    
    for size_data in sizes_data:
        size, created = Size.objects.get_or_create(
            size=size_data['size'],
            defaults=size_data
        )
        if created:
            print(f"  ✅ Created size: {size.size}")
    
    # Step 4: Create Tax
    print("💰 Creating taxes...")
    taxes_data = [
        {'tax_desc': 'Standard Tax', 'tax_value': Decimal('15.00'), 'status': True},
        {'tax_desc': 'Luxury Tax', 'tax_value': Decimal('20.00'), 'status': True},
    ]
    
    for tax_data in taxes_data:
        tax, created = Tax.objects.get_or_create(
            tax_desc=tax_data['tax_desc'],
            defaults=tax_data
        )
        if created:
            print(f"  ✅ Created tax: {tax.tax_desc}")
    
    # Step 5: Create Order Statuses
    print("📋 Creating order statuses...")
    order_statuses_data = [
        {'orders_status': 'Pending', 'is_default': True},
        {'orders_status': 'Processing', 'is_default': False},
        {'orders_status': 'Shipped', 'is_default': False},
        {'orders_status': 'Delivered', 'is_default': False},
        {'orders_status': 'Cancelled', 'is_default': False},
        {'orders_status': 'Returned', 'is_default': False},
    ]
    
    for status_data in order_statuses_data:
        status, created = OrderStatus.objects.get_or_create(
            orders_status=status_data['orders_status'],
            defaults=status_data
        )
        if created:
            print(f"  ✅ Created order status: {status.orders_status}")
    
    # Step 6: Create Categories
    print("📂 Creating categories...")
    categories_data = [
        {
            'category_name': 'Book Holders',
            'category_slug': 'book-holders',
            'parent_category': None,
            'is_home': True,
            'status': True
        },
        {
            'category_name': 'Business Card Holders',
            'category_slug': 'business-card-holders',
            'parent_category': None,
            'is_home': True,
            'status': True
        },
        {
            'category_name': 'Custom Name Plates',
            'category_slug': 'custom-name-plates',
            'parent_category': None,
            'is_home': True,
            'status': True
        },
        {
            'category_name': 'Glasses Holders',
            'category_slug': 'glasses-holders',
            'parent_category': None,
            'is_home': True,
            'status': True
        },
        {
            'category_name': 'Headphone Stands',
            'category_slug': 'headphone-stands',
            'parent_category': None,
            'is_home': True,
            'status': True
        },
        {
            'category_name': 'Key Holders',
            'category_slug': 'key-holders',
            'parent_category': None,
            'is_home': True,
            'status': True
        },
        {
            'category_name': 'Laptop Stands',
            'category_slug': 'laptop-stands',
            'parent_category': None,
            'is_home': True,
            'status': True
        },
        {
            'category_name': 'Pen Holders',
            'category_slug': 'pen-holders',
            'parent_category': None,
            'is_home': True,
            'status': True
        },
        {
            'category_name': 'Wall Decor',
            'category_slug': 'wall-decor',
            'parent_category': None,
            'is_home': True,
            'status': True
        },
        {
            'category_name': 'Watch Holders',
            'category_slug': 'watch-holders',
            'parent_category': None,
            'is_home': True,
            'status': True
        },
        {
            'category_name': 'Wooden Wall Clocks',
            'category_slug': 'wooden-wall-clocks',
            'parent_category': None,
            'is_home': True,
            'status': True
        },
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            category_slug=cat_data['category_slug'],
            defaults=cat_data
        )
        if created:
            print(f"  ✅ Created category: {category.category_name}")
    
    # Step 7: Create Coupons
    print("🎫 Creating coupons...")
    coupons_data = [
        {
            'title': 'Welcome Discount',
            'code': 'WELCOME10',
            'value': Decimal('10.00'),
            'type': 'Per',
            'min_order_amt': Decimal('1000.00'),
            'is_one_time': False,
            'status': True
        },
        {
            'title': 'New Customer Special',
            'code': 'NEWCUST20',
            'value': Decimal('20.00'),
            'type': 'Per',
            'min_order_amt': Decimal('2000.00'),
            'is_one_time': True,
            'status': True
        },
        {
            'title': 'Bulk Order Discount',
            'code': 'BULK500',
            'value': Decimal('500.00'),
            'type': 'Value',
            'min_order_amt': Decimal('5000.00'),
            'is_one_time': False,
            'status': True
        },
        {
            'title': 'Save 10% Discount',
            'code': 'SAVE10D',
            'value': Decimal('10.00'),
            'type': 'Per',
            'min_order_amt': Decimal('1000.00'),
            'is_one_time': False,
            'status': True
        },
        {
            'title': 'Save 500 PKR',
            'code': 'SAVE500',
            'value': Decimal('500.00'),
            'type': 'Value',
            'min_order_amt': Decimal('2000.00'),
            'is_one_time': True,
            'status': True
        },
    ]
    
    for coupon_data in coupons_data:
        coupon, created = Coupon.objects.get_or_create(
            code=coupon_data['code'],
            defaults=coupon_data
        )
        if created:
            print(f"  ✅ Created coupon: {coupon.title}")
    
    # Step 8: Create Sample Products
    print("🛍️ Creating sample products...")
    
    # Get existing data
    brands = {brand.name: brand for brand in Brand.objects.all()}
    categories = {cat.category_slug: cat for cat in Category.objects.all()}
    colors = {color.color: color for color in Color.objects.all()}
    sizes = {size.size: size for size in Size.objects.all()}
    tax = Tax.objects.first()
    
    # Create sample products
    sample_products = [
        {
            'name': 'Wooden Book Holder - Premium Quality',
            'category_slug': 'book-holders',
            'brand': 'WoodCraft Pro',
            'model': 'WBH-001',
            'short_desc': 'Handcrafted wooden book holder perfect for organizing your books.',
            'desc': 'Beautiful handcrafted wooden book holder made from premium quality wood. Features a natural finish that enhances the wood grain. Perfect for organizing books on your desk or bookshelf.',
            'keywords': 'book holder, wooden, handcrafted, natural, desk organizer',
            'technical_specification': 'Material: Premium Wood, Finish: Natural, Dimensions: 8" x 6" x 4"',
            'uses': 'Desk organization, Book storage, Home decor',
            'warranty': '1 year manufacturer warranty',
            'lead_time': '3-5 business days',
            'base_price': Decimal('2000.00'),
            'base_mrp': Decimal('2500.00'),
            'attributes': [
                {
                    'sku': 'WBH-001-D2B-S',
                    'mrp': Decimal('2500.00'),
                    'price': Decimal('2000.00'),
                    'qty': 50,
                    'size': 'Small',
                    'color': '#D2B48C'  # Natural Wood
                },
                {
                    'sku': 'WBH-001-8B4-M',
                    'mrp': Decimal('3000.00'),
                    'price': Decimal('2500.00'),
                    'qty': 30,
                    'size': 'Medium',
                    'color': '#8B4513'  # Walnut
                }
            ]
        },
        {
            'name': 'Premium Business Card Holder - Walnut Finish',
            'category_slug': 'business-card-holders',
            'brand': 'Artisan Wood',
            'model': 'BCH-002',
            'short_desc': 'Elegant business card holder crafted from premium walnut wood.',
            'desc': 'Sophisticated business card holder crafted from premium walnut wood. Features a sleek design perfect for any professional setting.',
            'keywords': 'business card holder, professional, office, wooden, elegant',
            'technical_specification': 'Material: Premium Wood, Finish: Natural, Dimensions: 4" x 3" x 2"',
            'uses': 'Office organization, Professional meetings, Business networking',
            'warranty': '2 years manufacturer warranty',
            'lead_time': '2-3 business days',
            'base_price': Decimal('1500.00'),
            'base_mrp': Decimal('1800.00'),
            'attributes': [
                {
                    'sku': 'BCH-002-8B4-OS',
                    'mrp': Decimal('1800.00'),
                    'price': Decimal('1500.00'),
                    'qty': 40,
                    'size': 'One Size',
                    'color': '#8B4513'  # Walnut
                }
            ]
        }
    ]
    
    for product_data in sample_products:
        category = categories[product_data['category_slug']]
        brand = brands[product_data['brand']]
        
        # Generate unique slug
        unique_slug = generate_unique_slug(product_data['name'])
        
        # Create product
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'category': category,
                'brand': brand,
                'model': product_data['model'],
                'slug': unique_slug,
                'short_desc': product_data['short_desc'],
                'desc': product_data['desc'],
                'keywords': product_data['keywords'],
                'technical_specification': product_data['technical_specification'],
                'uses': product_data['uses'],
                'warranty': product_data['warranty'],
                'lead_time': product_data['lead_time'],
                'tax': tax,
                'is_promo': False,
                'is_featured': True,
                'is_discounted': False,
                'is_arrival': True,
                'status': True
            }
        )
        
        if created:
            print(f"  ✅ Created product: {product.name}")
            
            # Create product attributes
            for attr_data in product_data['attributes']:
                size_obj = sizes[attr_data['size']]
                color_obj = colors[attr_data['color']]
                
                ProductAttribute.objects.create(
                    product=product,
                    sku=attr_data['sku'],
                    mrp=attr_data['mrp'],
                    price=attr_data['price'],
                    qty=attr_data['qty'],
                    size=size_obj,
                    color=color_obj
                )
                print(f"    🏷️ Created attribute: {attr_data['sku']}")
        else:
            print(f"  ℹ️ Product already exists: {product.name}")
    
    # Display summary
    print("\n📊 DATA INSERTION SUMMARY:")
    print(f"  📦 Brands: {Brand.objects.count()}")
    print(f"  🎨 Colors: {Color.objects.count()}")
    print(f"  📏 Sizes: {Size.objects.count()}")
    print(f"  💰 Taxes: {Tax.objects.count()}")
    print(f"  📋 Order Statuses: {OrderStatus.objects.count()}")
    print(f"  📂 Categories: {Category.objects.count()}")
    print(f"  🎫 Coupons: {Coupon.objects.count()}")
    print(f"  🛍️ Products: {Product.objects.count()}")
    print(f"  🏷️ Product Attributes: {ProductAttribute.objects.count()}")
    print(f"  🖼️ Product Images: {ProductImage.objects.count()}")
    
    print("\n🎉 All data has been successfully inserted into the database!")

if __name__ == '__main__':
    try:
        insert_all_data()
    except Exception as e:
        print(f"❌ Error during data insertion: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
