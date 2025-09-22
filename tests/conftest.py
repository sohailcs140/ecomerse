"""
Pytest configuration and fixtures for the ecommerce API tests.
"""

import os
import django
from django.conf import settings

# Configure Django settings before importing anything else
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_api.settings.development')
    django.setup()

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Brand, Category, Color, Size, Tax, OrderStatus
from products.models import Product, ProductAttribute
from customers.models import Customer

User = get_user_model()


@pytest.fixture
def api_client():
    """Return an API client instance."""
    return APIClient()


@pytest.fixture
def user():
    """Create a test user."""
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return User.objects.create_user(
        username=f'testuser{unique_id}',
        email=f'test{unique_id}@example.com',
        password='testpass123',
        user_type='customer'
    )


@pytest.fixture
def admin_user():
    """Create an admin user."""
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return User.objects.create_user(
        username=f'admin{unique_id}',
        email=f'admin{unique_id}@example.com',
        password='adminpass123',
        user_type='admin',
        is_staff=True
    )


@pytest.fixture
def customer_user():
    """Create a test user with customer type."""
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    User = get_user_model()
    return User.objects.create_user(
        username=f'customer{unique_id}',
        email=f'customer{unique_id}@example.com',
        password='testpass123',
        user_type='customer',
        mobile='1234567890'
    )


@pytest.fixture
def customer(customer_user):
    """Get the customer profile (auto-created by signal)."""
    return customer_user.customer_profile


@pytest.fixture
def authenticated_client(api_client, customer_user):
    """Return an authenticated API client with customer user."""
    refresh = RefreshToken.for_user(customer_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Return an admin authenticated API client."""
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def brand():
    """Create a test brand."""
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return Brand.objects.create(
        name=f'TestBrand{unique_id}',
        status=True,
        is_home=True
    )


@pytest.fixture
def category():
    """Create a test category."""
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return Category.objects.create(
        category_name=f'TestCategory{unique_id}',
        category_slug=f'test-category-{unique_id}',
        status=True,
        is_home=True
    )


@pytest.fixture
def color():
    """Create a test color."""
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return Color.objects.create(
        color=f'TestColor{unique_id}',
        status=True
    )


@pytest.fixture
def size():
    """Create a test size."""
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return Size.objects.create(
        size=f'Size{unique_id}',
        status=True
    )


@pytest.fixture
def tax():
    """Create a test tax."""
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return Tax.objects.create(
        tax_desc=f'GST{unique_id}',
        tax_value=18.0,
        status=True
    )


@pytest.fixture
def order_status():
    """Create a test order status."""
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return OrderStatus.objects.create(
        orders_status=f'Status{unique_id}'
    )


@pytest.fixture
def product(category, brand, tax):
    """Create a test product."""
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return Product.objects.create(
        category=category,
        name=f'TestProduct{unique_id}',
        slug=f'test-product-{unique_id}',
        brand=brand,
        model=f'TestModel{unique_id}',
        short_desc='Test description',
        tax=tax,
        status=True,
        is_featured=True
    )


@pytest.fixture
def product_attribute(product, size, color):
    """Create a test product attribute."""
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return ProductAttribute.objects.create(
        product=product,
        sku=f'TEST-{unique_id}',
        mrp=1000.00,
        price=800.00,
        qty=10,
        size=size,
        color=color
    )
