"""
Unit tests for models.
"""

import pytest
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from core.models import Brand, Category, Color, Size, Tax, Coupon
from products.models import Product, ProductAttribute
from customers.models import Customer

User = get_user_model()


@pytest.mark.django_db
class TestBrandModel:
    """Test Brand model."""

    def test_brand_creation(self):
        """Test brand creation."""
        brand = Brand.objects.create(
            name='Nike',
            status=True,
            is_home=True
        )
        assert brand.name == 'Nike'
        assert brand.status is True
        assert brand.is_home is True
        assert str(brand) == 'Nike'

    def test_brand_ordering(self):
        """Test brand ordering."""
        Brand.objects.create(name='Zebra', status=True)
        Brand.objects.create(name='Adidas', status=True)
        
        brands = list(Brand.objects.all())
        assert brands[0].name == 'Adidas'
        assert brands[1].name == 'Zebra'


@pytest.mark.django_db
class TestCategoryModel:
    """Test Category model."""

    def test_category_creation(self):
        """Test category creation."""
        category = Category.objects.create(
            category_name='Electronics',
            category_slug='electronics',
            status=True
        )
        assert category.category_name == 'Electronics'
        assert category.category_slug == 'electronics'
        assert str(category) == 'Electronics'

    def test_category_hierarchy(self):
        """Test category parent-child relationship."""
        parent = Category.objects.create(
            category_name='Electronics',
            category_slug='electronics',
            status=True
        )
        child = Category.objects.create(
            category_name='Smartphones',
            category_slug='smartphones',
            parent_category=parent,
            status=True
        )
        
        assert child.parent_category == parent
        assert child in parent.subcategories.all()

    def test_category_slug_unique(self):
        """Test category slug uniqueness."""
        Category.objects.create(
            category_name='Electronics',
            category_slug='electronics',
            status=True
        )
        
        with pytest.raises(IntegrityError):
            Category.objects.create(
                category_name='Electronics 2',
                category_slug='electronics',  # Duplicate slug
                status=True
            )


@pytest.mark.django_db
class TestProductModel:
    """Test Product model."""

    def test_product_creation(self, category, brand, tax):
        """Test product creation."""
        product = Product.objects.create(
            category=category,
            name='iPhone 13',
            slug='iphone-13',
            brand=brand,
            model='iPhone 13 Pro',
            short_desc='Latest iPhone',
            tax=tax,
            status=True
        )
        
        assert product.name == 'iPhone 13'
        assert product.slug == 'iphone-13'
        assert product.category == category
        assert product.brand == brand
        assert str(product) == 'iPhone 13'

    def test_product_slug_auto_generation(self, category, brand, tax):
        """Test automatic slug generation."""
        product = Product.objects.create(
            category=category,
            name='Test Product Name',
            brand=brand,
            model='Test Model',
            short_desc='Test description',
            tax=tax,
            status=True
        )
        
        assert product.slug == 'test-product-name'


@pytest.mark.django_db
class TestProductAttributeModel:
    """Test ProductAttribute model."""

    def test_product_attribute_creation(self, product, size, color):
        """Test product attribute creation."""
        attr = ProductAttribute.objects.create(
            product=product,
            sku='TEST-001',
            mrp=1000.00,
            price=800.00,
            qty=10,
            size=size,
            color=color
        )
        
        assert attr.product == product
        assert attr.sku == 'TEST-001'
        assert attr.mrp == 1000.00
        assert attr.price == 800.00
        assert attr.qty == 10
        assert str(attr) == f'{product.name} - TEST-001'

    def test_sku_unique(self, product, size, color):
        """Test SKU uniqueness."""
        ProductAttribute.objects.create(
            product=product,
            sku='UNIQUE-001',
            mrp=1000.00,
            price=800.00,
            qty=10,
            size=size,
            color=color
        )
        
        with pytest.raises(IntegrityError):
            ProductAttribute.objects.create(
                product=product,
                sku='UNIQUE-001',  # Duplicate SKU
                mrp=1000.00,
                price=800.00,
                qty=10,
                size=size,
                color=color
            )


@pytest.mark.django_db
class TestUserModel:
    """Test custom User model."""

    def test_user_creation(self):
        """Test user creation."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type='customer',
            mobile='1234567890'
        )
        
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.user_type == 'customer'
        assert user.mobile == '1234567890'
        assert user.check_password('testpass123')

    def test_user_str_representation(self):
        """Test user string representation."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type='customer'
        )
        
        assert str(user) == 'testuser (customer)'


@pytest.mark.django_db
class TestCustomerModel:
    """Test Customer model with User relationship."""

    def test_customer_auto_creation_via_signal(self):
        """Test automatic customer profile creation via signal."""
        user = User.objects.create_user(
            username='autocustomer',
            email='auto@example.com',
            password='testpass123',
            user_type='customer',
            mobile='1234567890'
        )
        
        # Customer profile should be auto-created by signal
        assert hasattr(user, 'customer_profile')
        customer = user.customer_profile
        
        assert customer.user == user
        assert customer.name == 'autocustomer'  # Default to username
        assert customer.email == 'auto@example.com'  # From property
        assert customer.is_active == True  # From property
        assert str(customer) == 'autocustomer (auto@example.com)'

    def test_admin_user_no_customer_profile(self):
        """Test that admin users don't get customer profiles."""
        admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpass123',
            user_type='admin'
        )
        
        # Admin should not have customer profile
        assert not hasattr(admin_user, 'customer_profile')

    def test_customer_user_relationship(self):
        """Test the one-to-one relationship between User and Customer."""
        user = User.objects.create_user(
            username='relationtest',
            email='relation@example.com',
            password='testpass123',
            user_type='customer'
        )
        
        # Customer should be auto-created
        customer = user.customer_profile
        
        # Test forward relationship
        assert customer.user == user
        
        # Test reverse relationship
        assert user.customer_profile == customer
        
        # Test properties
        assert customer.email == user.email
        assert customer.is_active == user.is_active

    def test_customer_profile_update(self):
        """Test updating customer profile."""
        user = User.objects.create_user(
            username='updatetest',
            email='update@example.com',
            password='testpass123',
            user_type='customer'
        )
        
        customer = user.customer_profile
        
        # Update customer profile
        customer.name = 'Updated Name'
        customer.mobile = '9999999999'
        customer.address = '456 New Street'
        customer.city = 'New City'
        customer.save()
        
        # Verify updates
        customer.refresh_from_db()
        assert customer.name == 'Updated Name'
        assert customer.mobile == '9999999999'
        assert customer.address == '456 New Street'
        assert customer.city == 'New City'


@pytest.mark.django_db
class TestCouponModel:
    """Test Coupon model."""

    def test_coupon_creation(self):
        """Test coupon creation."""
        coupon = Coupon.objects.create(
            title='Test Coupon',
            code='TEST10',
            value=10.00,
            type='Per',
            min_order_amt=100.00,
            status=True
        )
        
        assert coupon.title == 'Test Coupon'
        assert coupon.code == 'TEST10'
        assert coupon.value == 10.00
        assert coupon.type == 'Per'
        assert str(coupon) == 'Test Coupon (TEST10)'

    def test_coupon_code_unique(self):
        """Test coupon code uniqueness."""
        Coupon.objects.create(
            title='Test Coupon 1',
            code='UNIQUE',
            value=10.00,
            type='Per',
            min_order_amt=100.00,
            status=True
        )
        
        with pytest.raises(IntegrityError):
            Coupon.objects.create(
                title='Test Coupon 2',
                code='UNIQUE',  # Duplicate code
                value=15.00,
                type='Value',
                min_order_amt=200.00,
                status=True
            )
