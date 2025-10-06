"""
Single Django management command to insert all data into the database.
This command creates brands, categories, colors, sizes, taxes, coupons, order statuses,
and products with images from the upload-data directory.
"""

from django.core.management.base import BaseCommand
from django.core.files import File
import os
import shutil
import time
import random
from decimal import Decimal

from core.models import Brand, Category, Color, Size, Tax, Coupon, OrderStatus
from products.models import Product, ProductAttribute, ProductImage


class Command(BaseCommand):
    help = 'Insert all data into the database (brands, categories, colors, sizes, taxes, coupons, order statuses, and products)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-products',
            action='store_true',
            help='Skip product creation and only create core data',
        )
        parser.add_argument(
            '--skip-images',
            action='store_true',
            help='Skip image copying and only create product records',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting comprehensive data insertion...'))
        
        # Get the base directory for media files
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        media_dir = os.path.join(base_dir, 'media')
        upload_data_dir = os.path.join(media_dir, 'upload-data')
        
        # Step 1: Create Brands
        self.create_brands()
        
        # Step 2: Create Colors with hex values
        self.create_colors()
        
        # Step 3: Create Sizes
        self.create_sizes()
        
        # Step 4: Create Tax
        self.create_tax()
        
        # Step 5: Create Order Statuses
        self.create_order_statuses()
        
        # Step 6: Create Categories
        self.create_categories()
        
        # Step 7: Create Coupons
        self.create_coupons()
        
        # Step 8: Create Products (if not skipped)
        if not options['skip_products']:
            self.create_products_with_images(upload_data_dir, media_dir, options['skip_images'])
        
        self.stdout.write(self.style.SUCCESS('✅ All data insertion completed successfully!'))
        
        # Display summary
        self.display_summary()

    def generate_unique_slug(self, product_name):
        """Generate a unique slug for a product."""
        base_slug = f"{product_name.lower().replace(' ', '-').replace(',', '').replace('(', '').replace(')', '')}"
        unique_slug = f"{base_slug}-{int(time.time())}-{random.randint(1000, 9999)}"
        
        counter = 1
        original_slug = unique_slug
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{original_slug}-{counter}"
            counter += 1
        
        return unique_slug

    def create_brands(self):
        """Create brands."""
        self.stdout.write('📦 Creating brands...')
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
                self.stdout.write(f"  ✅ Created brand: {brand.name}")

    def create_colors(self):
        """Create colors with hex values."""
        self.stdout.write('🎨 Creating colors with hex values...')
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
                self.stdout.write(f"  ✅ Created color: {color.color}")

    def create_sizes(self):
        """Create sizes."""
        self.stdout.write('📏 Creating sizes...')
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
                self.stdout.write(f"  ✅ Created size: {size.size}")

    def create_tax(self):
        """Create tax."""
        self.stdout.write('💰 Creating taxes...')
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
                self.stdout.write(f"  ✅ Created tax: {tax.tax_desc}")

    def create_order_statuses(self):
        """Create order statuses."""
        self.stdout.write('📋 Creating order statuses...')
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
                self.stdout.write(f"  ✅ Created order status: {status.orders_status}")

    def create_categories(self):
        """Create categories."""
        self.stdout.write('📂 Creating categories...')
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
                self.stdout.write(f"  ✅ Created category: {category.category_name}")

    def create_coupons(self):
        """Create coupons."""
        self.stdout.write('🎫 Creating coupons...')
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
                self.stdout.write(f"  ✅ Created coupon: {coupon.title}")

    def create_products_with_images(self, upload_data_dir, media_dir, skip_images=False):
        """Create products with images from upload-data directory."""
        self.stdout.write('🛍️ Creating products with images...')
        
        # Get existing data
        brands = {brand.name: brand for brand in Brand.objects.all()}
        categories = {cat.category_slug: cat for cat in Category.objects.all()}
        colors = {color.color: color for color in Color.objects.all()}
        sizes = {size.size: size for size in Size.objects.all()}
        tax = Tax.objects.first()
        
        # Product data mapping based on folder names
        product_mappings = {
            'book holder': {
                'category_slug': 'book-holders',
                'brand': 'WoodCraft Pro',
                'base_name': 'Wooden Book Holder',
                'base_price': Decimal('2000.00'),
                'base_mrp': Decimal('2500.00'),
                'description': 'Handcrafted wooden book holder perfect for organizing your books and maintaining a tidy workspace.',
                'keywords': 'book holder, wooden, handcrafted, desk organizer, bookshelf',
                'technical_spec': 'Material: Premium Wood, Finish: Natural, Dimensions: 8" x 6" x 4"',
                'uses': 'Desk organization, Book storage, Home decor, Office setup',
                'warranty': '1 year manufacturer warranty',
                'lead_time': '3-5 business days'
            },
            'business card holders': {
                'category_slug': 'business-card-holders',
                'brand': 'Artisan Wood',
                'base_name': 'Premium Business Card Holder',
                'base_price': Decimal('1500.00'),
                'base_mrp': Decimal('1800.00'),
                'description': 'Elegant business card holder crafted from premium wood, perfect for professional settings.',
                'keywords': 'business card holder, professional, office, wooden, elegant',
                'technical_spec': 'Material: Premium Wood, Finish: Natural, Dimensions: 4" x 3" x 2"',
                'uses': 'Office organization, Professional meetings, Business networking',
                'warranty': '2 years manufacturer warranty',
                'lead_time': '2-3 business days'
            },
            'customize name plate': {
                'category_slug': 'custom-name-plates',
                'brand': 'Handmade Heritage',
                'base_name': 'Custom Engraved Name Plate',
                'base_price': Decimal('3000.00'),
                'base_mrp': Decimal('3500.00'),
                'description': 'Personalized wooden name plate with custom engraving, perfect for offices and homes.',
                'keywords': 'name plate, custom, engraved, personalized, wooden, office',
                'technical_spec': 'Material: Premium Wood, Custom Engraving: Yes, Dimensions: 6" x 2" x 0.5"',
                'uses': 'Office identification, Home decor, Personalized gifts',
                'warranty': '1 year manufacturer warranty',
                'lead_time': '7-10 business days'
            },
            'glasseshoders': {
                'category_slug': 'glasses-holders',
                'brand': 'WoodCraft Pro',
                'base_name': 'Wooden Glasses Holder',
                'base_price': Decimal('1200.00'),
                'base_mrp': Decimal('1500.00'),
                'description': 'Convenient wooden holder for eyeglasses with a small tray for accessories.',
                'keywords': 'glasses holder, eyeglasses, wooden, tray, accessories',
                'technical_spec': 'Material: Premium Wood, Tray: Yes, Dimensions: 6" x 4" x 2"',
                'uses': 'Glasses storage, Nightstand organizer, Bedroom decor',
                'warranty': '1 year manufacturer warranty',
                'lead_time': '3-5 business days'
            },
            'headphone stand': {
                'category_slug': 'headphone-stands',
                'brand': 'Premium Woodworks',
                'base_name': 'Premium Headphone Stand',
                'base_price': Decimal('2500.00'),
                'base_mrp': Decimal('3000.00'),
                'description': 'Stylish wooden headphone stand designed to keep your headphones organized and protected.',
                'keywords': 'headphone stand, wooden, gaming, audio, desk organizer',
                'technical_spec': 'Material: Premium Wood, Weight Capacity: 2kg, Dimensions: 8" x 6" x 12"',
                'uses': 'Gaming setup, Audio equipment organization, Desk organization',
                'warranty': '1 year manufacturer warranty',
                'lead_time': '5-7 business days'
            },
            'key holders': {
                'category_slug': 'key-holders',
                'brand': 'Artisan Wood',
                'base_name': 'Wooden Key Holder',
                'base_price': Decimal('1800.00'),
                'base_mrp': Decimal('2200.00'),
                'description': 'Beautiful wooden key holder with multiple hooks for organizing your keys.',
                'keywords': 'key holder, wooden, hooks, wall mount, organization',
                'technical_spec': 'Material: Premium Wood, Hooks: 6, Mount: Wall, Dimensions: 12" x 4" x 1"',
                'uses': 'Key organization, Entryway decor, Wall mounting',
                'warranty': '1 year manufacturer warranty',
                'lead_time': '3-5 business days'
            },
            'laptop stand': {
                'category_slug': 'laptop-stands',
                'brand': 'Premium Woodworks',
                'base_name': 'Adjustable Laptop Stand',
                'base_price': Decimal('3800.00'),
                'base_mrp': Decimal('4500.00'),
                'description': 'Ergonomic wooden laptop stand with adjustable height for comfortable working.',
                'keywords': 'laptop stand, adjustable, ergonomic, wooden, workspace',
                'technical_spec': 'Material: Premium Wood, Adjustable: Yes, Max Weight: 5kg, Dimensions: 12" x 8" x 2-6"',
                'uses': 'Laptop ergonomics, Workspace organization, Health and comfort',
                'warranty': '1 year manufacturer warranty',
                'lead_time': '5-7 business days'
            },
            'pen holders': {
                'category_slug': 'pen-holders',
                'brand': 'WoodCraft Pro',
                'base_name': 'Wooden Pen Holder',
                'base_price': Decimal('800.00'),
                'base_mrp': Decimal('1000.00'),
                'description': 'Classic wooden pen holder perfect for organizing writing instruments on your desk.',
                'keywords': 'pen holder, wooden, desk organizer, writing, office',
                'technical_spec': 'Material: Premium Wood, Capacity: 10 pens, Dimensions: 3" x 3" x 4"',
                'uses': 'Pen organization, Desk setup, Office organization',
                'warranty': '1 year manufacturer warranty',
                'lead_time': '2-3 business days'
            },
            'wall decore': {
                'category_slug': 'wall-decor',
                'brand': 'Handmade Heritage',
                'base_name': 'Wooden Wall Decor',
                'base_price': Decimal('2000.00'),
                'base_mrp': Decimal('2500.00'),
                'description': 'Beautiful wooden wall decoration pieces to enhance your home interior.',
                'keywords': 'wall decor, wooden, home decor, interior, decoration',
                'technical_spec': 'Material: Premium Wood, Finish: Natural, Mount: Wall, Dimensions: Various',
                'uses': 'Home decoration, Interior design, Wall mounting',
                'warranty': '1 year manufacturer warranty',
                'lead_time': '5-7 business days'
            },
            'watch holder': {
                'category_slug': 'watch-holders',
                'brand': 'Artisan Wood',
                'base_name': 'Wooden Watch Holder',
                'base_price': Decimal('1500.00'),
                'base_mrp': Decimal('1800.00'),
                'description': 'Elegant wooden watch holder with multiple slots for organizing your timepieces.',
                'keywords': 'watch holder, wooden, timepiece, organization, luxury',
                'technical_spec': 'Material: Premium Wood, Slots: 3, Dimensions: 8" x 4" x 2"',
                'uses': 'Watch storage, Jewelry organization, Bedroom decor',
                'warranty': '1 year manufacturer warranty',
                'lead_time': '3-5 business days'
            },
            'wooden wall cloack': {
                'category_slug': 'wooden-wall-clocks',
                'brand': 'Handmade Heritage',
                'base_name': 'Wooden Wall Clock',
                'base_price': Decimal('4000.00'),
                'base_mrp': Decimal('5000.00'),
                'description': 'Handcrafted wooden wall clock combining functionality with beautiful design.',
                'keywords': 'wall clock, wooden, handcrafted, timepiece, home decor',
                'technical_spec': 'Material: Premium Wood, Movement: Quartz, Diameter: 12", Battery: AA',
                'uses': 'Time keeping, Home decoration, Wall mounting',
                'warranty': '2 years manufacturer warranty',
                'lead_time': '7-10 business days'
            }
        }
        
        # Process each folder in upload-data
        if os.path.exists(upload_data_dir):
            for folder_name in os.listdir(upload_data_dir):
                folder_path = os.path.join(upload_data_dir, folder_name)
                
                if os.path.isdir(folder_path):
                    # Find matching product mapping
                    product_config = None
                    for key, config in product_mappings.items():
                        if key.lower() in folder_name.lower() or folder_name.lower() in key.lower():
                            product_config = config
                            break
                    
                    if not product_config:
                        self.stdout.write(f"  ⚠️ No product mapping found for folder: {folder_name}")
                        continue
                    
                    # Get category and brand
                    category = categories.get(product_config['category_slug'])
                    brand = brands.get(product_config['brand'])
                    
                    if not category or not brand:
                        self.stdout.write(f"  ⚠️ Category or brand not found for {folder_name}")
                        continue
                    
                    # Get image files
                    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
                    
                    if not image_files:
                        self.stdout.write(f"  ⚠️ No images found in {folder_name}")
                        continue
                    
                    # Create product name based on folder and first image
                    first_image = image_files[0]
                    product_name = f"{product_config['base_name']} - {folder_name.title()}"
                    
                    # Generate unique slug
                    unique_slug = self.generate_unique_slug(product_name)
                    
                    # Create product
                    product, created = Product.objects.get_or_create(
                        name=product_name,
                        defaults={
                            'category': category,
                            'brand': brand,
                            'model': f"{folder_name.upper().replace(' ', '-')}-001",
                            'slug': unique_slug,
                            'short_desc': product_config['description'][:100] + '...',
                            'desc': product_config['description'],
                            'keywords': product_config['keywords'],
                            'technical_specification': product_config['technical_spec'],
                            'uses': product_config['uses'],
                            'warranty': product_config['warranty'],
                            'lead_time': product_config['lead_time'],
                            'tax': tax,
                            'is_promo': False,
                            'is_featured': True,
                            'is_discounted': False,
                            'is_arrival': True,
                            'status': True
                        }
                    )
                    
                    if created:
                        self.stdout.write(f"  ✅ Created product: {product.name}")
                        
                        # Set main product image (if not skipping images)
                        if not skip_images:
                            main_image_path = os.path.join(folder_path, first_image)
                            if os.path.exists(main_image_path):
                                # Copy image to media/products/ directory
                                products_dir = os.path.join(media_dir, 'products')
                                os.makedirs(products_dir, exist_ok=True)
                                
                                new_image_name = f"{product.slug}_{first_image}"
                                new_image_path = os.path.join(products_dir, new_image_name)
                                
                                try:
                                    shutil.copy2(main_image_path, new_image_path)
                                    product.image = f'products/{new_image_name}'
                                    product.save()
                                    self.stdout.write(f"    📷 Set main image: {new_image_name}")
                                except Exception as e:
                                    self.stdout.write(f"    ❌ Error copying main image: {e}")
                        
                        # Create product attributes
                        colors_to_use = ['#D2B48C', '#8B4513', '#DEB887']  # Natural Wood, Walnut, Oak
                        sizes_to_use = ['Small', 'Medium', 'Large']
                        
                        for i, color_hex in enumerate(colors_to_use[:2]):  # Use first 2 colors
                            for j, size_name in enumerate(sizes_to_use[:2]):  # Use first 2 sizes
                                color_obj = colors.get(color_hex)
                                size_obj = sizes.get(size_name)
                                
                                # Calculate price variations
                                price_multiplier = 1 + (i * 0.2) + (j * 0.3)  # Color and size variations
                                price = product_config['base_price'] * Decimal(str(price_multiplier))
                                mrp = product_config['base_mrp'] * Decimal(str(price_multiplier))
                                
                                # Create a short color code from hex (remove # and take first 3 chars)
                                color_code = color_hex.replace('#', '')[:3].upper()
                                sku = f"{product.model}-{color_code}-{size_name[:1].upper()}"
                                
                                ProductAttribute.objects.create(
                                    product=product,
                                    sku=sku,
                                    mrp=mrp,
                                    price=price,
                                    qty=20 + (i * 10) + (j * 5),  # Vary quantity
                                    size=size_obj,
                                    color=color_obj
                                )
                                self.stdout.write(f"    🏷️ Created attribute: {sku}")
                        
                        # Create additional product images (if not skipping images)
                        if not skip_images:
                            for image_file in image_files[1:4]:  # Take up to 3 additional images
                                image_path = os.path.join(folder_path, image_file)
                                if os.path.exists(image_path):
                                    # Copy image to media/products/gallery/ directory
                                    gallery_dir = os.path.join(media_dir, 'products', 'gallery')
                                    os.makedirs(gallery_dir, exist_ok=True)
                                    
                                    new_image_name = f"{product.slug}_{image_file}"
                                    new_image_path = os.path.join(gallery_dir, new_image_name)
                                    
                                    try:
                                        shutil.copy2(image_path, new_image_path)
                                        
                                        # Create ProductImage record
                                        ProductImage.objects.create(
                                            product=product,
                                            image=f'products/gallery/{new_image_name}'
                                        )
                                        self.stdout.write(f"    🖼️ Added gallery image: {new_image_name}")
                                    except Exception as e:
                                        self.stdout.write(f"    ❌ Error copying gallery image: {e}")
                    else:
                        self.stdout.write(f"  ℹ️ Product already exists: {product.name}")
        else:
            self.stdout.write(f"  ⚠️ Upload data directory not found: {upload_data_dir}")

    def display_summary(self):
        """Display summary of created data."""
        self.stdout.write(self.style.SUCCESS('\n📊 DATA INSERTION SUMMARY:'))
        self.stdout.write(f"  📦 Brands: {Brand.objects.count()}")
        self.stdout.write(f"  🎨 Colors: {Color.objects.count()}")
        self.stdout.write(f"  📏 Sizes: {Size.objects.count()}")
        self.stdout.write(f"  💰 Taxes: {Tax.objects.count()}")
        self.stdout.write(f"  📋 Order Statuses: {OrderStatus.objects.count()}")
        self.stdout.write(f"  📂 Categories: {Category.objects.count()}")
        self.stdout.write(f"  🎫 Coupons: {Coupon.objects.count()}")
        self.stdout.write(f"  🛍️ Products: {Product.objects.count()}")
        self.stdout.write(f"  🏷️ Product Attributes: {ProductAttribute.objects.count()}")
        self.stdout.write(f"  🖼️ Product Images: {ProductImage.objects.count()}")
        
        self.stdout.write(self.style.SUCCESS('\n🎉 All data has been successfully inserted into the database!'))
