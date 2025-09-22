"""
Management command to populate initial data from the ecom.json file.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
import json
import os
from datetime import datetime

from core.models import Brand, Category, Color, Size, Tax, Coupon, HomeBanner, OrderStatus
from customers.models import Customer, Admin
from products.models import Product, ProductAttribute, ProductImage, ProductReview
from orders.models import Order, OrderDetail, Cart


class Command(BaseCommand):
    help = 'Populate initial data from ecom.json file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='ecom.json',
            help='Path to the JSON file containing data'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'File {file_path} not found')
            )
            return

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            with transaction.atomic():
                self.populate_data(data)
                
            self.stdout.write(
                self.style.SUCCESS('Successfully populated initial data')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error populating data: {str(e)}')
            )

    def populate_data(self, data):
        """Populate data from JSON structure."""
        
        for table_data in data:
            if table_data.get('type') != 'table':
                continue
                
            table_name = table_data.get('name')
            records = table_data.get('data', [])
            
            self.stdout.write(f'Processing table: {table_name}')
            
            # Process each table based on its name
            if table_name == 'brands':
                self.populate_brands(records)
            elif table_name == 'categories':
                self.populate_categories(records)
            elif table_name == 'colors':
                self.populate_colors(records)
            elif table_name == 'sizes':
                self.populate_sizes(records)
            elif table_name == 'taxs':
                self.populate_taxes(records)
            elif table_name == 'coupons':
                self.populate_coupons(records)
            elif table_name == 'home_banners':
                self.populate_home_banners(records)
            elif table_name == 'orders_status':
                self.populate_order_status(records)
            # Add more table processors as needed

    def populate_brands(self, records):
        """Populate brands table."""
        for record in records:
            Brand.objects.get_or_create(
                id=record['id'],
                defaults={
                    'name': record['name'],
                    'image': record.get('image', ''),
                    'status': bool(int(record['status'])),
                    'is_home': bool(int(record['is_home'])),
                }
            )

    def populate_categories(self, records):
        """Populate categories table."""
        # First pass: create categories without parent relationships
        for record in records:
            Category.objects.get_or_create(
                id=record['id'],
                defaults={
                    'category_name': record['category_name'],
                    'category_slug': record['category_slug'],
                    'category_image': record.get('category_image', ''),
                    'is_home': bool(int(record['is_home'])),
                    'status': bool(int(record['status'])),
                }
            )
        
        # Second pass: update parent relationships
        for record in records:
            if record['parent_category_id'] != '0':
                try:
                    category = Category.objects.get(id=record['id'])
                    parent = Category.objects.get(id=record['parent_category_id'])
                    category.parent_category = parent
                    category.save()
                except Category.DoesNotExist:
                    pass

    def populate_colors(self, records):
        """Populate colors table."""
        for record in records:
            Color.objects.get_or_create(
                id=record['id'],
                defaults={
                    'color': record['color'],
                    'status': bool(int(record['status'])),
                }
            )

    def populate_sizes(self, records):
        """Populate sizes table."""
        for record in records:
            Size.objects.get_or_create(
                id=record['id'],
                defaults={
                    'size': record['size'],
                    'status': bool(int(record['status'])),
                }
            )

    def populate_taxes(self, records):
        """Populate taxes table."""
        for record in records:
            Tax.objects.get_or_create(
                id=record['id'],
                defaults={
                    'tax_desc': record['tax_desc'],
                    'tax_value': record['tax_value'],
                    'status': bool(int(record['status'])),
                }
            )

    def populate_coupons(self, records):
        """Populate coupons table."""
        for record in records:
            Coupon.objects.get_or_create(
                id=record['id'],
                defaults={
                    'title': record['title'],
                    'code': record['code'],
                    'value': record['value'],
                    'type': record['type'],
                    'min_order_amt': record['min_order_amt'],
                    'is_one_time': bool(int(record['is_one_time'])),
                    'status': bool(int(record['status'])),
                }
            )

    def populate_home_banners(self, records):
        """Populate home banners table."""
        for record in records:
            HomeBanner.objects.get_or_create(
                id=record['id'],
                defaults={
                    'image': record['image'],
                    'btn_txt': record.get('btn_txt'),
                    'btn_link': record.get('btn_link'),
                    'status': bool(int(record['status'])),
                }
            )

    def populate_order_status(self, records):
        """Populate order status table."""
        for record in records:
            OrderStatus.objects.get_or_create(
                id=record['id'],
                defaults={
                    'orders_status': record['orders_status'],
                }
            )
