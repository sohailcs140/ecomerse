"""
Core URLs for the ecommerce application.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BrandViewSet, CategoryViewSet, ColorViewSet, SizeViewSet,
    TaxViewSet, CouponViewSet, HomeBannerViewSet, OrderStatusViewSet
)

router = DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'colors', ColorViewSet)
router.register(r'sizes', SizeViewSet)
router.register(r'taxes', TaxViewSet)
router.register(r'coupons', CouponViewSet)
router.register(r'banners', HomeBannerViewSet)
router.register(r'order-status', OrderStatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
