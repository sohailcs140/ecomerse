"""
API views for core functionality.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    API root endpoint with information about available endpoints.
    """
    return Response({
        'message': 'Welcome to Ecommerce API',
        'version': '1.0.0',
        'documentation': {
            'swagger': request.build_absolute_uri('/api/docs/'),
            'redoc': request.build_absolute_uri('/api/redoc/'),
            'schema': request.build_absolute_uri('/api/schema/'),
        },
        'endpoints': {
            'authentication': request.build_absolute_uri('/api/v1/auth/'),
            'core': request.build_absolute_uri('/api/v1/core/'),
            'products': request.build_absolute_uri('/api/v1/products/'),
            'orders': request.build_absolute_uri('/api/v1/orders/'),
            'customers': request.build_absolute_uri('/api/v1/customers/'),
        },
        'examples': {
            'product_list': request.build_absolute_uri('/api/v1/products/products/'),
            'product_detail': request.build_absolute_uri('/api/v1/products/products/{slug}/'),
            'featured_products': request.build_absolute_uri('/api/v1/products/products/featured/'),
        },
        'admin': request.build_absolute_uri('/admin/'),
        'debug': settings.DEBUG
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint.
    """
    return Response({
        'status': 'healthy',
        'timestamp': request.META.get('HTTP_DATE'),
        'version': '1.0.0'
    })
