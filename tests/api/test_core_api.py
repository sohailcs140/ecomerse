"""
API tests for core endpoints.
"""

import pytest
from django.urls import reverse
from rest_framework import status

from core.models import Brand, Category, Coupon, HomeBanner


@pytest.mark.django_db
class TestBrandAPI:
    """Test brand API endpoints."""

    def test_list_brands(self, api_client, brand):
        """Test listing brands."""
        url = reverse('brand-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == brand.name

    def test_brand_detail(self, api_client, brand):
        """Test brand detail endpoint."""
        url = reverse('brand-detail', kwargs={'pk': brand.pk})
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == brand.name
        assert response.data['status'] == brand.status

    def test_home_brands(self, api_client, brand):
        """Test home brands endpoint."""
        url = reverse('brand-home-brands')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == brand.name

    def test_search_brands(self, api_client, brand):
        """Test searching brands."""
        url = reverse('brand-list')
        
        response = api_client.get(url, {'search': 'Test'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_create_brand_unauthorized(self, api_client):
        """Test creating brand without authentication."""
        url = reverse('brand-list')
        data = {
            'name': 'New Brand',
            'status': True,
            'is_home': False
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCategoryAPI:
    """Test category API endpoints."""

    def test_list_categories(self, api_client, category):
        """Test listing categories."""
        url = reverse('category-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['category_name'] == category.category_name

    def test_main_categories(self, api_client, category):
        """Test main categories endpoint."""
        url = reverse('category-main-categories')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['category_name'] == category.category_name

    def test_home_categories(self, api_client, category):
        """Test home categories endpoint."""
        url = reverse('category-home-categories')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['category_name'] == category.category_name

    def test_category_with_subcategories(self, api_client, category):
        """Test category with subcategories."""
        # Create a subcategory
        subcategory = Category.objects.create(
            category_name='Subcategory',
            category_slug='subcategory',
            parent_category=category,
            status=True
        )
        
        url = reverse('category-detail', kwargs={'pk': category.pk})
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['subcategories']) == 1
        assert response.data['subcategories'][0]['category_name'] == subcategory.category_name

    def test_filter_categories_by_parent(self, api_client, category):
        """Test filtering categories by parent."""
        # Create a subcategory
        subcategory = Category.objects.create(
            category_name='Subcategory',
            category_slug='subcategory',
            parent_category=category,
            status=True
        )
        
        url = reverse('category-list')
        
        response = api_client.get(url, {'parent_category': category.id})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['category_name'] == subcategory.category_name


@pytest.mark.django_db
class TestColorAPI:
    """Test color API endpoints."""

    def test_list_colors(self, api_client, color):
        """Test listing colors."""
        url = reverse('color-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['color'] == color.color

    def test_search_colors(self, api_client, color):
        """Test searching colors."""
        url = reverse('color-list')
        
        response = api_client.get(url, {'search': 'Red'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1


@pytest.mark.django_db
class TestSizeAPI:
    """Test size API endpoints."""

    def test_list_sizes(self, api_client, size):
        """Test listing sizes."""
        url = reverse('size-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['size'] == size.size


@pytest.mark.django_db
class TestCouponAPI:
    """Test coupon API endpoints."""

    def test_list_coupons_unauthorized(self, api_client):
        """Test listing coupons without authentication."""
        url = reverse('coupon-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_coupons_authorized(self, authenticated_client):
        """Test listing coupons with authentication."""
        # Create a coupon
        Coupon.objects.create(
            title='Test Coupon',
            code='TEST10',
            value=10.00,
            type='Per',
            min_order_amt=100.00,
            status=True
        )
        
        url = reverse('coupon-list')
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1

    def test_validate_coupon_valid(self, authenticated_client):
        """Test validating a valid coupon."""
        # Create a coupon
        Coupon.objects.create(
            title='Test Coupon',
            code='VALID10',
            value=10.00,
            type='Per',
            min_order_amt=100.00,
            status=True
        )
        
        url = reverse('coupon-validate-coupon')
        data = {
            'code': 'VALID10',
            'order_amount': 200.00
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valid'] is True
        assert response.data['discount'] == 20.00  # 10% of 200
        assert 'coupon' in response.data

    def test_validate_coupon_invalid_code(self, authenticated_client):
        """Test validating an invalid coupon code."""
        url = reverse('coupon-validate-coupon')
        data = {
            'code': 'INVALID',
            'order_amount': 200.00
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valid'] is False
        assert 'Invalid coupon code' in response.data['message']

    def test_validate_coupon_minimum_order(self, authenticated_client):
        """Test validating coupon with insufficient order amount."""
        # Create a coupon with minimum order amount
        Coupon.objects.create(
            title='Test Coupon',
            code='MIN500',
            value=50.00,
            type='Value',
            min_order_amt=500.00,
            status=True
        )
        
        url = reverse('coupon-validate-coupon')
        data = {
            'code': 'MIN500',
            'order_amount': 300.00  # Less than minimum
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valid'] is False
        assert 'Minimum order amount' in response.data['message']

    def test_validate_fixed_value_coupon(self, authenticated_client):
        """Test validating a fixed value coupon."""
        # Create a fixed value coupon
        Coupon.objects.create(
            title='Fixed Coupon',
            code='FIXED50',
            value=50.00,
            type='Value',
            min_order_amt=100.00,
            status=True
        )
        
        url = reverse('coupon-validate-coupon')
        data = {
            'code': 'FIXED50',
            'order_amount': 200.00
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valid'] is True
        assert response.data['discount'] == 50.00  # Fixed value


@pytest.mark.django_db
class TestHomeBannerAPI:
    """Test home banner API endpoints."""

    def test_list_home_banners(self, api_client):
        """Test listing home banners."""
        # Create a banner
        HomeBanner.objects.create(
            image='test_banner.jpg',
            btn_txt='Shop Now',
            btn_link='http://example.com',
            status=True
        )
        
        url = reverse('homebanner-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['btn_txt'] == 'Shop Now'
