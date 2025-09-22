"""
Unit tests for serializers.
"""

import pytest
from django.contrib.auth import get_user_model

from core.serializers import BrandSerializer, CategorySerializer, CouponSerializer
from products.serializers import ProductListSerializer, ProductDetailSerializer
from accounts.serializers import UserRegistrationSerializer, UserLoginSerializer

User = get_user_model()


@pytest.mark.django_db
class TestBrandSerializer:
    """Test Brand serializer."""

    def test_brand_serialization(self, brand):
        """Test brand serialization."""
        serializer = BrandSerializer(brand)
        data = serializer.data
        
        assert data['name'] == brand.name
        assert data['status'] == brand.status
        assert data['is_home'] == brand.is_home

    def test_brand_deserialization(self):
        """Test brand deserialization."""
        data = {
            'name': 'New Brand',
            'status': True,
            'is_home': False
        }
        
        serializer = BrandSerializer(data=data)
        assert serializer.is_valid()
        
        brand = serializer.save()
        assert brand.name == 'New Brand'
        assert brand.status is True
        assert brand.is_home is False


@pytest.mark.django_db
class TestCategorySerializer:
    """Test Category serializer."""

    def test_category_with_subcategories(self, category):
        """Test category serialization with subcategories."""
        # Create a subcategory
        from core.models import Category
        subcategory = Category.objects.create(
            category_name='Subcategory',
            category_slug='subcategory',
            parent_category=category,
            status=True
        )
        
        serializer = CategorySerializer(category)
        data = serializer.data
        
        assert data['category_name'] == category.category_name
        assert len(data['subcategories']) == 1
        assert data['subcategories'][0]['category_name'] == subcategory.category_name

    def test_category_without_subcategories(self, category):
        """Test category serialization without subcategories."""
        serializer = CategorySerializer(category)
        data = serializer.data
        
        assert data['category_name'] == category.category_name
        assert data['subcategories'] == []


@pytest.mark.django_db
class TestProductSerializer:
    """Test Product serializers."""

    def test_product_list_serialization(self, product, product_attribute):
        """Test product list serialization."""
        serializer = ProductListSerializer(product)
        data = serializer.data
        
        assert data['name'] == product.name
        assert data['brand_name'] == product.brand.name
        assert data['category_name'] == product.category.category_name
        assert 'min_price' in data
        assert 'max_price' in data
        assert 'avg_rating' in data
        assert 'review_count' in data

    def test_product_detail_serialization(self, product):
        """Test product detail serialization."""
        serializer = ProductDetailSerializer(product)
        data = serializer.data
        
        assert data['name'] == product.name
        assert 'brand' in data
        assert 'category' in data
        assert 'tax' in data
        assert 'attributes' in data
        assert 'images' in data
        assert 'reviews' in data


@pytest.mark.django_db
class TestUserRegistrationSerializer:
    """Test User registration serializer."""

    def test_valid_registration_data(self):
        """Test valid registration data."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'confirm_password': 'newpass123',
            'user_type': 'customer',
            'mobile': '9876543210'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        assert serializer.is_valid()
        
        user = serializer.save()
        assert user.username == 'newuser'
        assert user.email == 'newuser@example.com'
        assert user.user_type == 'customer'

    def test_password_mismatch(self):
        """Test password mismatch validation."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'confirm_password': 'different123',
            'user_type': 'customer'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors

    def test_short_password(self):
        """Test short password validation."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': '123',
            'confirm_password': '123',
            'user_type': 'customer'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors


@pytest.mark.django_db
class TestCouponSerializer:
    """Test Coupon serializer."""

    def test_coupon_serialization(self):
        """Test coupon serialization."""
        from core.models import Coupon
        
        coupon = Coupon.objects.create(
            title='Test Coupon',
            code='TEST10',
            value=10.00,
            type='Per',
            min_order_amt=100.00,
            status=True
        )
        
        serializer = CouponSerializer(coupon)
        data = serializer.data
        
        assert data['title'] == coupon.title
        assert data['code'] == coupon.code
        assert float(data['value']) == float(coupon.value)
        assert data['type'] == coupon.type
