"""
API tests for order endpoints.
"""

import pytest
from django.urls import reverse
from rest_framework import status

from orders.models import Cart, Order, OrderDetail


@pytest.mark.django_db
class TestCartAPI:
    """Test cart API endpoints."""

    def test_get_cart_items(self, api_client, product, product_attribute):
        """Test getting cart items."""
        # Create cart item
        cart_item = Cart.objects.create(
            user_id='test_user_123',
            user_type='Not-Reg',
            qty=2,
            product=product,
            product_attr=product_attribute
        )
        
        url = reverse('cart-list')
        
        response = api_client.get(url, {'user_id': 'test_user_123'})
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['qty'] == 2

    def test_get_cart_total(self, api_client, product, product_attribute):
        """Test getting cart total."""
        # Create cart items
        Cart.objects.create(
            user_id='test_user_123',
            user_type='Not-Reg',
            qty=2,
            product=product,
            product_attr=product_attribute
        )
        
        url = reverse('cart-total')
        
        response = api_client.get(url, {'user_id': 'test_user_123'})
        
        assert response.status_code == status.HTTP_200_OK
        assert 'total' in response.data
        assert 'item_count' in response.data
        assert 'items' in response.data
        assert response.data['item_count'] == 1
        assert response.data['total'] == product_attribute.price * 2

    def test_add_item_to_cart(self, api_client, product, product_attribute):
        """Test adding item to cart."""
        url = reverse('cart-add-item')
        data = {
            'user_id': 'test_user_123',
            'user_type': 'Not-Reg',
            'product': product.id,
            'product_attr': product_attribute.id,
            'qty': 1
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Cart.objects.filter(user_id='test_user_123').count() == 1

    def test_add_existing_item_to_cart(self, api_client, product, product_attribute):
        """Test adding existing item to cart (should update quantity)."""
        # Create initial cart item
        Cart.objects.create(
            user_id='test_user_123',
            user_type='Not-Reg',
            qty=1,
            product=product,
            product_attr=product_attribute
        )
        
        url = reverse('cart-add-item')
        data = {
            'user_id': 'test_user_123',
            'user_type': 'Not-Reg',
            'product': product.id,
            'product_attr': product_attribute.id,
            'qty': 2
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        
        # Check that quantity was updated, not a new item created
        cart_items = Cart.objects.filter(user_id='test_user_123')
        assert cart_items.count() == 1
        assert cart_items.first().qty == 3  # 1 + 2

    def test_update_cart_quantity(self, api_client, product, product_attribute):
        """Test updating cart item quantity."""
        # Create cart item
        Cart.objects.create(
            user_id='test_user_123',
            user_type='Not-Reg',
            qty=2,
            product=product,
            product_attr=product_attribute
        )
        
        url = reverse('cart-update-quantity')
        data = {
            'user_id': 'test_user_123',
            'product_attr': product_attribute.id,
            'qty': 5
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify quantity was updated
        cart_item = Cart.objects.get(user_id='test_user_123')
        assert cart_item.qty == 5

    def test_remove_cart_item(self, api_client, product, product_attribute):
        """Test removing cart item by setting quantity to 0."""
        # Create cart item
        Cart.objects.create(
            user_id='test_user_123',
            user_type='Not-Reg',
            qty=2,
            product=product,
            product_attr=product_attribute
        )
        
        url = reverse('cart-update-quantity')
        data = {
            'user_id': 'test_user_123',
            'product_attr': product_attribute.id,
            'qty': 0
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'removed from cart' in response.data['message']
        
        # Verify item was removed
        assert Cart.objects.filter(user_id='test_user_123').count() == 0

    def test_clear_cart(self, api_client, product, product_attribute):
        """Test clearing all cart items."""
        # Create multiple cart items
        Cart.objects.create(
            user_id='test_user_123',
            user_type='Not-Reg',
            qty=1,
            product=product,
            product_attr=product_attribute
        )
        Cart.objects.create(
            user_id='test_user_123',
            user_type='Not-Reg',
            qty=2,
            product=product,
            product_attr=product_attribute
        )
        
        url = reverse('cart-clear-cart')
        
        response = api_client.delete(url, {'user_id': 'test_user_123'})
        
        assert response.status_code == status.HTTP_200_OK
        assert 'cleared successfully' in response.data['message']
        
        # Verify all items were removed
        assert Cart.objects.filter(user_id='test_user_123').count() == 0

    def test_cart_total_missing_user_id(self, api_client):
        """Test cart total without user_id parameter."""
        url = reverse('cart-total')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'user_id is required' in response.data['error']


@pytest.mark.django_db
class TestOrderAPI:
    """Test order API endpoints."""

    def test_list_orders_unauthorized(self, api_client):
        """Test listing orders without authentication."""
        url = reverse('order-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_orders_customer(self, authenticated_client, user, order_status):
        """Test listing orders as customer."""
        # Ensure user has customer profile
        if not hasattr(user, 'customer_profile'):
            from customers.models import Customer
            Customer.objects.create(
                user=user,
                name='Test Customer',
                mobile='1234567890'
            )
        
        # Create an order for the customer
        Order.objects.create(
            customer=user.customer_profile,
            name='Test Customer',
            email=user.email,
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
        
        url = reverse('order-list')
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1

    def test_create_order(self, authenticated_client, customer_user, order_status):
        """Test creating an order."""
        url = reverse('order-list')
        data = {
            'customer': customer_user.customer_profile.id,
            'name': 'Test Customer',
            'email': 'test@example.com',
            'mobile': '1234567890',
            'address': 'Test Address',
            'city': 'Test City',
            'state': 'Test State',
            'pincode': '123456',
            'order_status': order_status.id,
            'payment_type': 'COD',
            'payment_status': 'Pending',
            'total_amt': 1500.00
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Test Customer'
        assert response.data['total_amt'] == '1500.00'

    def test_my_orders(self, authenticated_client, customer_user, order_status):
        """Test getting current user's orders."""
        # Create orders
        Order.objects.create(
            customer=customer_user.customer_profile,
            name='Test Customer',
            email=customer_user.email,
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
        
        url = reverse('order-my-orders')
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1

    def test_update_order_status(self, admin_client, customer, order_status):
        """Test updating order status."""
        # Create an order
        order = Order.objects.create(
            customer=customer,
            name='Test Customer',
            email='test@example.com',
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
        
        # Create another order status
        from core.models import OrderStatus
        new_status = OrderStatus.objects.create(orders_status='Shipped')
        
        url = reverse('order-update-status', kwargs={'pk': order.pk})
        data = {
            'order_status': new_status.id,
            'track_details': 'Order has been shipped'
        }
        
        response = admin_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify order was updated
        order.refresh_from_db()
        assert order.order_status == new_status
        assert order.track_details == 'Order has been shipped'

    def test_filter_orders_by_status(self, admin_client, customer, order_status):
        """Test filtering orders by status."""
        # Create orders with different statuses
        Order.objects.create(
            customer=customer,
            name='Test Customer 1',
            email='test1@example.com',
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
        
        from core.models import OrderStatus
        shipped_status = OrderStatus.objects.create(orders_status='Shipped')
        Order.objects.create(
            customer=customer,
            name='Test Customer 2',
            email='test2@example.com',
            mobile='1234567890',
            address='Test Address',
            city='Test City',
            state='Test State',
            pincode='123456',
            order_status=shipped_status,
            payment_type='COD',
            payment_status='Pending',
            total_amt=2000.00
        )
        
        url = reverse('order-list')
        
        response = admin_client.get(url, {'order_status': order_status.id})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == 'Test Customer 1'
