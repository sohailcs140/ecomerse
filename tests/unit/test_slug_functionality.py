"""
Unit tests for slug functionality.
"""

import pytest
from django.urls import reverse
from rest_framework import status

from products.models import Product


@pytest.mark.django_db
class TestProductSlugFunctionality:
    """Test product slug functionality."""

    def test_product_slug_auto_generation(self, category, brand, tax):
        """Test automatic slug generation from product name."""
        product = Product.objects.create(
            category=category,
            name='iPhone 13 Pro Max',
            brand=brand,
            model='iPhone 13 Pro Max',
            short_desc='Latest iPhone',
            tax=tax,
            status=True
        )
        
        assert product.slug == 'iphone-13-pro-max'

    def test_product_slug_manual_setting(self, category, brand, tax):
        """Test manual slug setting."""
        product = Product.objects.create(
            category=category,
            name='Test Product',
            slug='custom-slug',
            brand=brand,
            model='Test Model',
            short_desc='Test description',
            tax=tax,
            status=True
        )
        
        assert product.slug == 'custom-slug'

    def test_product_slug_uniqueness(self, category, brand, tax):
        """Test that product slugs are unique."""
        import uuid
        unique_id1 = str(uuid.uuid4())[:8]
        unique_id2 = str(uuid.uuid4())[:8]
        
        # Create first product
        product1 = Product.objects.create(
            category=category,
            name=f'Test Product {unique_id1}',
            brand=brand,
            model='Test Model 1',
            short_desc='Test description 1',
            tax=tax,
            status=True
        )
        
        # Create second product with different name
        product2 = Product.objects.create(
            category=category,
            name=f'Test Product {unique_id2}',
            brand=brand,
            model='Test Model 2',
            short_desc='Test description 2',
            tax=tax,
            status=True
        )
        
        # Both should have different slugs
        assert product1.slug != product2.slug
        assert unique_id1.lower() in product1.slug
        assert unique_id2.lower() in product2.slug

    def test_product_detail_by_slug_api(self, api_client, product):
        """Test accessing product detail via slug in API."""
        url = reverse('product-detail', kwargs={'slug': product.slug})
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['slug'] == product.slug
        assert response.data['name'] == product.name

    def test_product_detail_nonexistent_slug(self, api_client):
        """Test accessing non-existent product slug."""
        url = reverse('product-detail', kwargs={'slug': 'non-existent-product'})
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_product_detail_invalid_slug_format(self, api_client):
        """Test accessing product with invalid slug format."""
        url = reverse('product-detail', kwargs={'slug': 'Invalid Slug With Spaces'})
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_slug_in_product_list_response(self, api_client, product):
        """Test that slug is included in product list response."""
        url = reverse('product-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1
        assert 'slug' in response.data['results'][0]
        assert response.data['results'][0]['slug'] == product.slug

    def test_slug_consistency_across_endpoints(self, api_client, product):
        """Test that slug is consistent across list and detail endpoints."""
        # Get product from list
        list_url = reverse('product-list')
        list_response = api_client.get(list_url)
        product_from_list = list_response.data['results'][0]
        
        # Get same product from detail
        detail_url = reverse('product-detail', kwargs={'slug': product.slug})
        detail_response = api_client.get(detail_url)
        
        assert product_from_list['slug'] == detail_response.data['slug']
        assert product_from_list['name'] == detail_response.data['name']
