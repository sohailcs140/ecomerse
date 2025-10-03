"""
Product views for the ecommerce application.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from .models import Product, ProductAttribute, ProductImage, ProductReview
from .serializers import (
    ProductListSerializer, ProductDetailSerializer, ProductCreateUpdateSerializer,
    ProductAttributeSerializer, ProductImageSerializer, ProductReviewSerializer
)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Product viewset with advanced filtering and search.
    """
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'brand', 'is_featured', 'is_promo', 'is_discounted', 'is_arrival']
    search_fields = ['name', 'keywords', 'short_desc']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductListSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products."""
        products = self.queryset.filter(is_featured=True)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Get trending products."""
        products = self.queryset.filter(is_tranding=True)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def discounted(self, request):
        """Get discounted products."""
        products = self.queryset.filter(is_discounted=True)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search_advanced(self, request):
        """Advanced search with price range and other filters."""
        queryset = self.queryset
        # Price range filter
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        ordering = request.query_params.get("ordering")

        if min_price:
            queryset = queryset.filter(attributes__price__gte=min_price)
        if max_price:
            queryset = queryset.filter(attributes__price__lte=max_price)
            
        # Category filter
        categories = request.query_params.getlist('categories')
        if categories:
            queryset = queryset.filter(category__id__in=categories)
            
        # Brand filter
        brands = request.query_params.getlist('brands')
        if brands:
            queryset = queryset.filter(brand__id__in=brands)
            
        # Color filter
        colors = request.query_params.getlist('colors')
        if colors:
            queryset = queryset.filter(attributes__color__id__in=colors)
            
        # Size filter
        sizes = request.query_params.getlist('sizes')
        if sizes:
            queryset = queryset.filter(attributes__size__id__in=sizes)

        queryset = queryset.distinct()

        if ordering:
            queryset = queryset.order_by(ordering)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductReviewViewSet(viewsets.ModelViewSet):
    """
    Product review viewset.
    """
    queryset = ProductReview.objects.filter(status=True)
    serializer_class = ProductReviewSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['product', 'rating']
    ordering = ['-added_on']

    def get_permissions(self):
        """Allow public read access, require authentication for write operations."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer_profile)


class ProductAttributeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Product attribute viewset (read-only).
    """
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'size', 'color']
    permission_classes = [permissions.AllowAny]  # Public read access