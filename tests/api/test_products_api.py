"""
API tests for product endpoints.
"""

import pytest
from django.urls import reverse
from rest_framework import status

from products.models import Product, ProductReview


@pytest.mark.django_db
class TestProductsAPI:
    """Test products API endpoints."""

    def test_list_products(self, api_client, product):
        """Test listing products."""
        url = reverse('product-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == product.name

    def test_product_detail(self, api_client, product):
        """Test product detail endpoint."""
        url = reverse('product-detail', kwargs={'slug': product.slug})
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == product.name
        assert 'brand' in response.data
        assert 'category' in response.data
        assert 'attributes' in response.data

    def test_product_search(self, api_client, product):
        """Test product search functionality."""
        url = reverse('product-list')
        
        response = api_client.get(url, {'search': 'Test'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == product.name

    def test_product_filter_by_category(self, api_client, product):
        """Test filtering products by category."""
        url = reverse('product-list')
        
        response = api_client.get(url, {'category': product.category.id})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == product.name

    def test_product_filter_by_brand(self, api_client, product):
        """Test filtering products by brand."""
        url = reverse('product-list')
        
        response = api_client.get(url, {'brand': product.brand.id})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == product.name

    def test_featured_products(self, api_client, product):
        """Test featured products endpoint."""
        url = reverse('product-featured')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == product.name

    def test_trending_products(self, api_client, product):
        """Test trending products endpoint."""
        # First make the product trending
        product.is_tranding = True
        product.save()
        
        url = reverse('product-trending')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1

    def test_discounted_products(self, api_client, product):
        """Test discounted products endpoint."""
        # First make the product discounted
        product.is_discounted = True
        product.save()
        
        url = reverse('product-discounted')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1

    def test_advanced_search(self, api_client, product, product_attribute):
        """Test advanced search endpoint."""
        url = reverse('product-search-advanced')
        
        # Test price range filter
        response = api_client.get(url, {
            'min_price': 500,
            'max_price': 1000
        })
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data

    def test_create_product_unauthorized(self, api_client):
        """Test creating product without authentication."""
        url = reverse('product-list')
        data = {
            'name': 'New Product',
            'category': 1,
            'brand': 1,
            'model': 'New Model',
            'short_desc': 'Description',
            'tax': 1
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_product_authorized(self, admin_client, category, brand, tax):
        """Test creating product with admin authentication."""
        url = reverse('product-list')
        data = {
            'name': 'New Product',
            'category': category.id,
            'brand': brand.id,
            'model': 'New Model',
            'short_desc': 'Description',
            'tax': tax.id,
            'status': True
        }
        
        response = admin_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Product'


@pytest.mark.django_db
class TestProductReviewAPI:
    """Test product review API endpoints."""

    def test_list_product_reviews(self, api_client, product, customer):
        """Test listing product reviews."""
        # Create a review
        ProductReview.objects.create(
            customer=customer,
            product=product,
            rating='Very Good',
            review='Great product!',
            status=True
        )
        
        url = reverse('productreview-list')
        
        response = api_client.get(url, {'product': product.id})
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1

    def test_create_review_unauthorized(self, api_client, product):
        """Test creating review without authentication."""
        url = reverse('productreview-list')
        data = {
            'product': product.id,
            'rating': 'Very Good',
            'review': 'Great product!'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_filter_reviews_by_rating(self, api_client, product, customer):
        """Test filtering reviews by rating."""
        # Create reviews with different ratings
        ProductReview.objects.create(
            customer=customer,
            product=product,
            rating='Very Good',
            review='Great product!',
            status=True
        )
        ProductReview.objects.create(
            customer=customer,
            product=product,
            rating='Good',
            review='Nice product!',
            status=True
        )
        
        url = reverse('productreview-list')
        
        response = api_client.get(url, {'rating': 'Very Good'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['rating'] == 'Very Good'


@pytest.mark.django_db
class TestProductAttributeAPI:
    """Test product attribute API endpoints."""

    def test_list_product_attributes(self, api_client, product_attribute):
        """Test listing product attributes."""
        url = reverse('productattribute-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['sku'] == product_attribute.sku

    def test_filter_attributes_by_product(self, api_client, product_attribute):
        """Test filtering attributes by product."""
        url = reverse('productattribute-list')
        
        response = api_client.get(url, {'product': product_attribute.product.id})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['product'] == product_attribute.product.id

    def test_filter_attributes_by_color(self, api_client, product_attribute):
        """Test filtering attributes by color."""
        url = reverse('productattribute-list')
        
        response = api_client.get(url, {'color': product_attribute.color.id})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['color'] == product_attribute.color.id
