"""
Integration tests for complete ecommerce flow.
"""

import pytest
from django.urls import reverse
from rest_framework import status

from orders.models import Cart, Order
from products.models import Product, ProductAttribute


@pytest.mark.django_db
class TestEcommerceFlow:
    """Test complete ecommerce user flow."""

    def test_complete_shopping_flow(self, api_client, product, product_attribute, order_status):
        """Test complete shopping flow from registration to order."""
        
        # Step 1: User Registration
        register_url = reverse('register')
        register_data = {
            'username': 'shopuser',
            'email': 'shop@example.com',
            'password': 'shoppass123',
            'confirm_password': 'shoppass123',
            'user_type': 'customer',
            'mobile': '9876543210'
        }
        
        response = api_client.post(register_url, register_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # Get tokens for authentication
        access_token = response.data['tokens']['access']
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # Step 2: Browse Products
        products_url = reverse('product-list')
        response = api_client.get(products_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        
        # Step 3: View Product Details
        product_detail_url = reverse('product-detail', kwargs={'slug': product.slug})
        response = api_client.get(product_detail_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == product.name
        
        # Step 4: Add to Cart
        add_to_cart_url = reverse('cart-add-item')
        cart_data = {
            'user_id': 'shopuser_123',
            'user_type': 'Reg',
            'product': product.id,
            'product_attr': product_attribute.id,
            'qty': 2
        }
        
        response = api_client.post(add_to_cart_url, cart_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # Step 5: View Cart
        cart_total_url = reverse('cart-total')
        response = api_client.get(cart_total_url, {'user_id': 'shopuser_123'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['item_count'] == 1
        assert response.data['total'] == product_attribute.price * 2
        
        # Step 6: Update Cart Quantity
        update_cart_url = reverse('cart-update-quantity')
        update_data = {
            'user_id': 'shopuser_123',
            'product_attr': product_attribute.id,
            'qty': 3
        }
        
        response = api_client.post(update_cart_url, update_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        # Verify updated quantity
        response = api_client.get(cart_total_url, {'user_id': 'shopuser_123'})
        assert response.data['total'] == product_attribute.price * 3
        
        # Step 7: Get Customer Profile (auto-created during registration)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Get the user we created during registration
        user = User.objects.get(email='shop@example.com')
        customer = user.customer_profile
        
        # Step 8: Place Order
        order_url = reverse('order-list')
        order_data = {
            'customer': customer.id,
            'name': 'Shop User',
            'email': 'shop@example.com',
            'mobile': '9876543210',
            'address': '123 Test Street',
            'city': 'Test City',
            'state': 'Test State',
            'pincode': '123456',
            'order_status': order_status.id,
            'payment_type': 'COD',
            'payment_status': 'Pending',
            'total_amt': product_attribute.price * 3
        }
        
        response = api_client.post(order_url, order_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['total_amt'] == str(product_attribute.price * 3)
        
        # Step 9: View Order History
        my_orders_url = reverse('order-my-orders')
        response = api_client.get(my_orders_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_guest_shopping_flow(self, api_client, product, product_attribute):
        """Test guest user shopping flow."""
        
        # Step 1: Browse Products (no authentication needed)
        products_url = reverse('product-list')
        response = api_client.get(products_url)
        assert response.status_code == status.HTTP_200_OK
        
        # Step 2: Add to Cart as Guest
        add_to_cart_url = reverse('cart-add-item')
        cart_data = {
            'user_id': 'guest_session_123',
            'user_type': 'Not-Reg',
            'product': product.id,
            'product_attr': product_attribute.id,
            'qty': 1
        }
        
        response = api_client.post(add_to_cart_url, cart_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # Step 3: View Cart
        cart_total_url = reverse('cart-total')
        response = api_client.get(cart_total_url, {'user_id': 'guest_session_123'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['item_count'] == 1
        
        # Step 4: Clear Cart
        clear_cart_url = reverse('cart-clear-cart')
        response = api_client.delete(clear_cart_url, {'user_id': 'guest_session_123'})
        assert response.status_code == status.HTTP_200_OK
        
        # Verify cart is empty
        response = api_client.get(cart_total_url, {'user_id': 'guest_session_123'})
        assert response.data['item_count'] == 0

    def test_product_search_and_filter_flow(self, api_client, product, product_attribute):
        """Test product search and filtering flow."""
        
        # Create additional test data
        from core.models import Brand, Category, Tax
        
        brand2 = Brand.objects.create(name='Brand 2', status=True)
        category2 = Category.objects.create(
            category_name='Category 2',
            category_slug='category-2',
            status=True
        )
        tax = Tax.objects.create(tax_desc='GST 18%', tax_value=18.0, status=True)
        
        product2 = Product.objects.create(
            category=category2,
            name='Another Product',
            slug='another-product',
            brand=brand2,
            model='Another Model',
            short_desc='Another description',
            tax=tax,
            status=True,
            is_featured=False,
            is_discounted=True
        )
        
        # Step 1: Search Products
        products_url = reverse('product-list')
        response = api_client.get(products_url, {'search': 'Test'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1  # Only original product matches
        
        # Step 2: Filter by Category
        response = api_client.get(products_url, {'category': product.category.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        
        # Step 3: Filter by Brand
        response = api_client.get(products_url, {'brand': product.brand.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        
        # Step 4: Get Featured Products
        featured_url = reverse('product-featured')
        response = api_client.get(featured_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1  # Only original product is featured
        
        # Step 5: Get Discounted Products
        discounted_url = reverse('product-discounted')
        response = api_client.get(discounted_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1  # Only product2 is discounted
        assert response.data['results'][0]['name'] == 'Another Product'

    def test_admin_order_management_flow(self, admin_client, customer, order_status):
        """Test admin order management flow."""
        
        # Step 1: Create an Order
        order = Order.objects.create(
            customer=customer,
            name='Test Customer',
            email='customer@example.com',
            mobile='1234567890',
            address='Test Address',
            city='Test City',
            state='Test State',
            pincode='123456',
            order_status=order_status,
            payment_type='COD',
            payment_status='Pending',
            total_amt=1000.00
        )
        
        # Step 2: View All Orders (Admin)
        orders_url = reverse('order-list')
        response = admin_client.get(orders_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        
        # Step 3: Filter Orders by Status
        response = admin_client.get(orders_url, {'order_status': order_status.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        
        # Step 4: Update Order Status
        from core.models import OrderStatus
        shipped_status = OrderStatus.objects.create(orders_status='Shipped')
        
        update_status_url = reverse('order-update-status', kwargs={'pk': order.pk})
        update_data = {
            'order_status': shipped_status.id,
            'track_details': 'Order shipped via Express Delivery'
        }
        
        response = admin_client.patch(update_status_url, update_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        # Verify order was updated
        order.refresh_from_db()
        assert order.order_status == shipped_status
        assert 'Express Delivery' in order.track_details
