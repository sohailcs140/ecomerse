"""
Data migration to populate initial data for the ecommerce application.
This migration creates categories, brands, colors, sizes, taxes, and other core data
based on the images in media/upload-data/ directory.
"""

from django.db import migrations
from django.core.files import File
import os
from decimal import Decimal


def populate_initial_data(apps, schema_editor):
    """
    Populate the database with initial data.
    """
    # Get models
    Brand = apps.get_model('core', 'Brand')
    Category = apps.get_model('core', 'Category')
    Color = apps.get_model('core', 'Color')
    Size = apps.get_model('core', 'Size')
    Tax = apps.get_model('core', 'Tax')
    Coupon = apps.get_model('core', 'Coupon')
    OrderStatus = apps.get_model('core', 'OrderStatus')
    Product = apps.get_model('products', 'Product')
    ProductAttribute = apps.get_model('products', 'ProductAttribute')
    ProductImage = apps.get_model('products', 'ProductImage')
    
    # Get the base directory for media files
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    media_dir = os.path.join(base_dir, 'media')
    upload_data_dir = os.path.join(media_dir, 'upload-data')
    
    # Create Brands
    brands_data = [
        {'name': 'WoodCraft Pro', 'status': True, 'is_home': True},
        {'name': 'Artisan Wood', 'status': True, 'is_home': True},
        {'name': 'Premium Woodworks', 'status': True, 'is_home': False},
        {'name': 'Handmade Heritage', 'status': True, 'is_home': True},
    ]
    
    brands = {}
    for brand_data in brands_data:
        brand, created = Brand.objects.get_or_create(
            name=brand_data['name'],
            defaults=brand_data
        )
        brands[brand_data['name']] = brand
        print(f"Created brand: {brand.name}")
    
    # Create Colors with hex values
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
    ]
    
    colors = {}
    for color_data in colors_data:
        color, created = Color.objects.get_or_create(
            color=color_data['color'],
            defaults=color_data
        )
        colors[color_data['color']] = color
        print(f"Created color: {color.color}")
    
    # Create Sizes
    sizes_data = [
        {'size': 'Small', 'status': True},
        {'size': 'Medium', 'status': True},
        {'size': 'Large', 'status': True},
        {'size': 'Extra Large', 'status': True},
        {'size': 'One Size', 'status': True},
    ]
    
    sizes = {}
    for size_data in sizes_data:
        size, created = Size.objects.get_or_create(
            size=size_data['size'],
            defaults=size_data
        )
        sizes[size_data['size']] = size
        print(f"Created size: {size.size}")
    
    # Create Tax
    tax, created = Tax.objects.get_or_create(
        tax_desc='Standard Tax',
        defaults={
            'tax_value': Decimal('15.00'),
            'status': True
        }
    )
    print(f"Created tax: {tax.tax_desc}")
    
    # Create Order Statuses
    order_statuses_data = [
        {'orders_status': 'Pending', 'is_default': True},
        {'orders_status': 'Processing', 'is_default': False},
        {'orders_status': 'Shipped', 'is_default': False},
        {'orders_status': 'Delivered', 'is_default': False},
        {'orders_status': 'Cancelled', 'is_default': False},
    ]
    
    for status_data in order_statuses_data:
        status, created = OrderStatus.objects.get_or_create(
            orders_status=status_data['orders_status'],
            defaults=status_data
        )
        print(f"Created order status: {status.orders_status}")
    
    # Create Categories based on folder names
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
    
    categories = {}
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            category_slug=cat_data['category_slug'],
            defaults=cat_data
        )
        categories[cat_data['category_slug']] = category
        print(f"Created category: {category.category_name}")
    
    # Create additional coupons
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
    ]
    
    for coupon_data in coupons_data:
        coupon, created = Coupon.objects.get_or_create(
            code=coupon_data['code'],
            defaults=coupon_data
        )
        print(f"Created coupon: {coupon.title}")
    
    # Create sample products for each category
    products_data = [
        {
            'category_slug': 'book-holders',
            'name': 'Wooden Book Holder - Natural Finish',
            'brand': 'WoodCraft Pro',
            'model': 'WBH-001',
            'short_desc': 'Handcrafted wooden book holder with natural finish',
            'desc': 'Beautiful handcrafted wooden book holder made from premium quality wood. Features a natural finish that enhances the wood grain. Perfect for organizing books on your desk or bookshelf.',
            'keywords': 'book holder, wooden, handcrafted, natural, desk organizer',
            'technical_specification': 'Material: Premium Wood, Finish: Natural, Dimensions: 8" x 6" x 4"',
            'uses': 'Desk organization, Book storage, Home decor',
            'warranty': '1 year manufacturer warranty',
            'lead_time': '3-5 business days',
            'is_promo': False,
            'is_featured': True,
            'is_discounted': False,
            'is_arrival': True,
            'status': True,
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
                    'sku': 'WBH-001-D2B-M',
                    'mrp': Decimal('3000.00'),
                    'price': Decimal('2500.00'),
                    'qty': 30,
                    'size': 'Medium',
                    'color': '#D2B48C'  # Natural Wood
                },
                {
                    'sku': 'WBH-001-8B4-M',
                    'mrp': Decimal('3500.00'),
                    'price': Decimal('3000.00'),
                    'qty': 25,
                    'size': 'Medium',
                    'color': '#8B4513'  # Walnut
                }
            ]
        },
        {
            'category_slug': 'business-card-holders',
            'name': 'Premium Business Card Holder - Walnut',
            'brand': 'Artisan Wood',
            'model': 'BCH-002',
            'short_desc': 'Elegant walnut business card holder for professional use',
            'desc': 'Sophisticated business card holder crafted from premium walnut wood. Features a sleek design perfect for any professional setting.',
            'keywords': 'business card holder, walnut, professional, office, wooden',
            'technical_specification': 'Material: Walnut Wood, Finish: Natural, Dimensions: 4" x 3" x 2"',
            'uses': 'Office organization, Professional meetings, Business networking',
            'warranty': '2 years manufacturer warranty',
            'lead_time': '2-3 business days',
            'is_promo': True,
            'is_featured': True,
            'is_discounted': True,
            'is_arrival': False,
            'status': True,
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
        },
        {
            'category_slug': 'laptop-stands',
            'name': 'Adjustable Laptop Stand - Bamboo',
            'brand': 'Premium Woodworks',
            'model': 'LS-003',
            'short_desc': 'Eco-friendly bamboo laptop stand with adjustable height',
            'desc': 'Sustainable bamboo laptop stand designed for ergonomic comfort. Features adjustable height and angle for optimal viewing position.',
            'keywords': 'laptop stand, bamboo, adjustable, ergonomic, eco-friendly',
            'technical_specification': 'Material: Bamboo, Adjustable: Yes, Max Weight: 5kg, Dimensions: 12" x 8" x 2-6"',
            'uses': 'Laptop ergonomics, Workspace organization, Health and comfort',
            'warranty': '1 year manufacturer warranty',
            'lead_time': '5-7 business days',
            'is_promo': False,
            'is_featured': True,
            'is_discounted': False,
            'is_arrival': True,
            'status': True,
            'attributes': [
                {
                    'sku': 'LS-003-9AC-M',
                    'mrp': Decimal('4500.00'),
                    'price': Decimal('3800.00'),
                    'qty': 20,
                    'size': 'Medium',
                    'color': '#9ACD32'  # Bamboo
                }
            ]
        }
    ]
    
    # Create products
    for product_data in products_data:
        category = categories[product_data['category_slug']]
        brand = brands[product_data['brand']]
        
        # Create main product with unique slug
        def generate_unique_slug(product_name):
            import time
            import random
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
        
        unique_slug = generate_unique_slug(product_data['name'])
        
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
                'is_promo': product_data['is_promo'],
                'is_featured': product_data['is_featured'],
                'is_discounted': product_data['is_discounted'],
                'is_arrival': product_data['is_arrival'],
                'status': product_data['status']
            }
        )
        
        if created:
            print(f"Created product: {product.name}")
            
            # Create product attributes
            for attr_data in product_data['attributes']:
                size_obj = sizes[attr_data['size']] if attr_data['size'] in sizes else None
                color_obj = colors[attr_data['color']] if attr_data['color'] in colors else None
                
                ProductAttribute.objects.create(
                    product=product,
                    sku=attr_data['sku'],
                    mrp=attr_data['mrp'],
                    price=attr_data['price'],
                    qty=attr_data['qty'],
                    size=size_obj,
                    color=color_obj
                )
                print(f"Created attribute: {attr_data['sku']}")
    
    print("Initial data population completed successfully!")


def reverse_populate_initial_data(apps, schema_editor):
    """
    Reverse the data population (optional - for rollback).
    """
    # Get models
    Brand = apps.get_model('core', 'Brand')
    Category = apps.get_model('core', 'Category')
    Color = apps.get_model('core', 'Color')
    Size = apps.get_model('core', 'Size')
    Tax = apps.get_model('core', 'Tax')
    Coupon = apps.get_model('core', 'Coupon')
    OrderStatus = apps.get_model('core', 'OrderStatus')
    Product = apps.get_model('products', 'Product')
    
    # Delete created data (be careful with this in production)
    Product.objects.filter(name__contains='Wooden Book Holder').delete()
    Product.objects.filter(name__contains='Premium Business Card Holder').delete()
    Product.objects.filter(name__contains='Adjustable Laptop Stand').delete()
    
    Coupon.objects.filter(code__in=['WELCOME10', 'NEWCUST20', 'BULK500']).delete()
    
    print("Initial data population reversed!")


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_orderstatus_is_default'),
        ('products', '0003_alter_product_brand_alter_product_model_and_more'),
    ]

    operations = [
        migrations.RunPython(
            populate_initial_data,
            reverse_populate_initial_data
        ),
    ]
