"""
Product URLs for the ecommerce application.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductReviewViewSet, ProductAttributeViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'reviews', ProductReviewViewSet)
router.register(r'attributes', ProductAttributeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
