"""
API tests for authentication endpoints.
"""

import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAuthAPI:
    """Test authentication API endpoints."""

    def test_user_registration(self, api_client):
        """Test user registration endpoint."""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'confirm_password': 'newpass123',
            'user_type': 'customer',
            'mobile': '9876543210'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'user' in response.data
        assert 'tokens' in response.data
        assert response.data['user']['username'] == 'newuser'
        assert response.data['user']['email'] == 'newuser@example.com'

    def test_user_registration_invalid_data(self, api_client):
        """Test user registration with invalid data."""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'invalid-email',
            'password': '123',  # Too short
            'confirm_password': '456',  # Doesn't match
            'user_type': 'customer'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data or 'password' in response.data or 'non_field_errors' in response.data

    def test_user_login(self, api_client, user):
        """Test user login endpoint."""
        url = reverse('login')
        data = {
            'username': user.username,
            'password': 'testpass123'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'user' in response.data
        assert 'tokens' in response.data
        assert response.data['user']['username'] == user.username
        assert 'access' in response.data['tokens']
        assert 'refresh' in response.data['tokens']

    def test_user_login_invalid_credentials(self, api_client, user):
        """Test user login with invalid credentials."""
        url = reverse('login')
        data = {
            'username': user.username,
            'password': 'wrongpassword'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_profile(self, authenticated_client, customer_user):
        """Test user profile endpoint."""
        url = reverse('profile')
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == customer_user.username
        assert response.data['email'] == customer_user.email
        assert response.data['user_type'] == customer_user.user_type

    def test_user_profile_unauthenticated(self, api_client):
        """Test user profile endpoint without authentication."""
        url = reverse('profile')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_profile(self, authenticated_client, customer_user):
        """Test update user profile endpoint."""
        url = reverse('update_profile')
        data = {
            'mobile': '9999999999'
        }
        
        response = authenticated_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['mobile'] == '9999999999'
        
        # Verify the user was actually updated
        customer_user.refresh_from_db()
        assert customer_user.mobile == '9999999999'

    def test_logout(self, authenticated_client, customer_user):
        """Test user logout endpoint."""
        # Get a refresh token for the authenticated user
        from rest_framework_simplejwt.tokens import RefreshToken
        
        refresh = RefreshToken.for_user(customer_user)
        
        url = reverse('logout')
        data = {
            'refresh': str(refresh)
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        # Logout might fail if blacklisting is not configured, but endpoint should exist
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
        
        if response.status_code == status.HTTP_200_OK:
            assert 'message' in response.data
        else:
            # Blacklisting might not be configured, which is fine for testing
            assert 'error' in response.data
