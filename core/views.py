"""
Core views for the ecommerce application.
"""

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Brand, Category, Color, Size, Tax, Coupon, HomeBanner, OrderStatus
from .serializers import (
    BrandSerializer, CategorySerializer, ColorSerializer, SizeSerializer,
    TaxSerializer, CouponSerializer, HomeBannerSerializer, OrderStatusSerializer, CategoryKpisSerializer
)
from .filters import CategoryFilter


class BrandViewSet(viewsets.ModelViewSet):
    """
    Brand viewset with CRUD operations.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    pagination_class = None
    
    def get_permissions(self):
        """Allow public read access, require authentication for write operations."""
        if self.action in ['list', 'retrieve', 'home_brands']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def home_brands(self, request):
        """Get brands displayed on homepage."""
        brands = self.queryset.filter(is_home=True)
        serializer = self.get_serializer(brands, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['parent_category__category_slug']  # use slug instead of id
    search_fields = ['category_name']
    ordering_fields = ['category_name', 'created_at']
    ordering = ['category_name']
    filterset_class = CategoryFilter
    lookup_field = "category_slug"
    lookup_url_kwarg = "category"
    pagination_class = None
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'main_categories', 'home_categories']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], url_path='main-categories')
    def main_categories(self, request):
        categories = self.queryset.filter(parent_category__isnull=True)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='home-categories')
    def home_categories(self, request):
        categories = self.queryset.filter(is_home=True)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='category-kpis')
    def get_category_kpis(self, request):
        kpis = CategoryKpisSerializer(instance={})
        print(kpis.data)
        return Response(kpis.data)



class ColorViewSet(viewsets.ModelViewSet):
    """
    Color viewset.
    """
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['color']
    ordering = ['color']
    pagination_class = None
    
    def get_permissions(self):
        """Allow public read access, require authentication for write operations."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class SizeViewSet(viewsets.ModelViewSet):
    """
    Size viewset.
    """
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['size']
    ordering = ['size']
    pagination_class = None

    def get_permissions(self):
        """Allow public read access, require authentication for write operations."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class TaxViewSet(viewsets.ModelViewSet):
    """
    Tax viewset.
    """
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

class CouponViewSet(viewsets.ModelViewSet):
    """
    Coupon viewset.
    """
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['code', 'title']
    pagination_class = None


    @action(detail=False, methods=['post'])
    def validate_coupon(self, request):
        """Validate coupon code."""
        code = request.data.get('code')
        order_amount = request.data.get('order_amount', 0)
        
        try:
            coupon = Coupon.objects.get(code=code, status=True)
            if order_amount < coupon.min_order_amt:
                return Response({
                    'valid': False, 
                    'message': f'Minimum order amount is {coupon.min_order_amt}'
                })
            
            discount = 0
            if coupon.type == 'Value':
                discount = coupon.value
            else:  # Percentage
                discount = (order_amount * coupon.value) / 100
                
            return Response({
                'valid': True,
                'discount': discount,
                'coupon': CouponSerializer(coupon).data
            })
        except Coupon.DoesNotExist:
            return Response({'valid': False, 'message': 'Invalid coupon code'})


class HomeBannerViewSet(viewsets.ModelViewSet):
    """
    Home banner viewset.
    """
    queryset = HomeBanner.objects.filter(status=True)
    serializer_class = HomeBannerSerializer
    ordering = ['id']
    pagination_class = None

    def get_permissions(self):
        """Allow public read access, require authentication for write operations."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]  
    


class OrderStatusViewSet(viewsets.ModelViewSet):
    """
    Order status viewset.
    """
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None