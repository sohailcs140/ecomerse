"""
Data migration to populate products with actual images from media/upload-data/ directory.
This migration creates products based on the folder structure and images available.
"""

from django.db import migrations
from django.core.files import File
import os
import shutil
from decimal import Decimal


def populate_products_with_images(apps, schema_editor):
    """
    Populate products with actual images from upload-data directory.
    """
    # Get models
    Brand = apps.get_model('core', 'Brand')
    Category = apps.get_model('core', 'Category')
    Color = apps.get_model('core', 'Color')
    Size = apps.get_model('core', 'Size')
    Tax = apps.get_model('core', 'Tax')
    Product = apps.get_model('products', 'Product')
    ProductAttribute = apps.get_model('products', 'ProductAttribute')
    ProductImage = apps.get_model('products', 'ProductImage')
    
    # Get the base directory for media files
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    media_dir = os.path.join(base_dir, 'media')
    upload_data_dir = os.path.join(media_dir, 'upload-data')
    
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
                    print(f"No product mapping found for folder: {folder_name}")
                    continue
                
                # Get category and brand
                category = categories.get(product_config['category_slug'])
                brand = brands.get(product_config['brand'])
                
                if not category or not brand:
                    print(f"Category or brand not found for {folder_name}")
                    continue
                
                # Get image files
                image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
                
                if not image_files:
                    print(f"No images found in {folder_name}")
                    continue
                
                # Create product name based on folder and first image
                first_image = image_files[0]
                product_name = f"{product_config['base_name']} - {folder_name.title()}"
                
                # Create product
                product, created = Product.objects.get_or_create(
                    name=product_name,
                    defaults={
                        'category': category,
                        'brand': brand,
                        'model': f"{folder_name.upper().replace(' ', '-')}-001",
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
                    print(f"Created product: {product.name}")
                    
                    # Set main product image
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
                            print(f"Set main image: {new_image_name}")
                        except Exception as e:
                            print(f"Error copying main image: {e}")
                    
                    # Create product attributes
                    colors_to_use = ['Natural Wood', 'Walnut', 'Oak']
                    sizes_to_use = ['Small', 'Medium', 'Large']
                    
                    for i, color_name in enumerate(colors_to_use[:2]):  # Use first 2 colors
                        for j, size_name in enumerate(sizes_to_use[:2]):  # Use first 2 sizes
                            color_obj = colors.get(color_name)
                            size_obj = sizes.get(size_name)
                            
                            # Calculate price variations
                            price_multiplier = 1 + (i * 0.2) + (j * 0.3)  # Color and size variations
                            price = product_config['base_price'] * Decimal(str(price_multiplier))
                            mrp = product_config['base_mrp'] * Decimal(str(price_multiplier))
                            
                            sku = f"{product.model}-{color_name[:3].upper()}-{size_name[:1].upper()}"
                            
                            ProductAttribute.objects.create(
                                product=product,
                                sku=sku,
                                mrp=mrp,
                                price=price,
                                qty=20 + (i * 10) + (j * 5),  # Vary quantity
                                size=size_obj,
                                color=color_obj
                            )
                            print(f"Created attribute: {sku}")
                    
                    # Create additional product images
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
                                print(f"Added gallery image: {new_image_name}")
                            except Exception as e:
                                print(f"Error copying gallery image: {e}")
                else:
                    print(f"Product already exists: {product.name}")
    
    print("Products with images population completed successfully!")


def reverse_populate_products_with_images(apps, schema_editor):
    """
    Reverse the products population.
    """
    Product = apps.get_model('products', 'Product')
    
    # Delete products created by this migration
    Product.objects.filter(name__contains='Wooden Book Holder').delete()
    Product.objects.filter(name__contains='Premium Business Card Holder').delete()
    Product.objects.filter(name__contains='Custom Engraved Name Plate').delete()
    Product.objects.filter(name__contains='Wooden Glasses Holder').delete()
    Product.objects.filter(name__contains='Premium Headphone Stand').delete()
    Product.objects.filter(name__contains='Wooden Key Holder').delete()
    Product.objects.filter(name__contains='Adjustable Laptop Stand').delete()
    Product.objects.filter(name__contains='Wooden Pen Holder').delete()
    Product.objects.filter(name__contains='Wooden Wall Decor').delete()
    Product.objects.filter(name__contains='Wooden Watch Holder').delete()
    Product.objects.filter(name__contains='Wooden Wall Clock').delete()
    
    print("Products with images population reversed!")


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_populate_initial_data'),
        ('products', '0003_alter_product_brand_alter_product_model_and_more'),
    ]

    operations = [
        migrations.RunPython(
            populate_products_with_images,
            reverse_populate_products_with_images
        ),
    ]
