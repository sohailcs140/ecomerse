"""
Order views for the ecommerce application.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView

from .models import Order, OrderDetail, Cart
from .serializers import OrderSerializer, OrderDetailSerializer, CartSerializer, CartAddSerializer
from products.models import ProductAttribute

from core.serializers import OrderStatusOverviewSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    Order viewset.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['order_status', 'payment_type', 'payment_status']
    ordering = ['-added_on']

    def get_queryset(self):
        # Handle swagger fake view generation
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
            
        if hasattr(self.request.user, 'user_type') and self.request.user.user_type == 'admin':
            return Order.objects.all()
        # For customers, only show their own orders
        try:
            return Order.objects.filter(user=self.request.user)
        except:
            return Order.objects.none()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update order status."""
        order = self.get_object()
        new_status = request.data.get('order_status')
        track_details = request.data.get('track_details', '')
        
        if new_status:
            order.order_status_id = new_status
            order.track_details = track_details
            order.save()
            
            serializer = self.get_serializer(order)
            return Response(serializer.data)
        
        return Response({'error': 'Order status is required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path="my-orders")
    def my_orders(self, request):
        """Get current user's orders."""
        orders = self.get_queryset()
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


class CartViewSet(viewsets.ModelViewSet):
    """
    Shopping cart viewset.
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny] 
    pagination_class = None
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Cart.objects.filter(user_id=user_id)
        return Cart.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return CartAddSerializer
        return CartSerializer

    @action(detail=False, methods=['get'])
    def total(self, request):
        """Get cart total."""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        cart_items = Cart.objects.filter(user_id=user_id)
        total = sum(item.product_attr.price * item.qty for item in cart_items)
        item_count = cart_items.count()
        
        return Response({
            'total': total,
            'item_count': item_count,
            'items': CartSerializer(cart_items, many=True).data
        })

    @action(detail=False, methods=['post'], url_path="add-item")
    def add_item(self, request):
        """Add item to cart or update quantity if exists."""
        user_id = request.data.get('user_id')
        product_id = request.data.get('product')
        product_attr_id = request.data.get('product_attr')
        qty = int(request.data.get('qty', 1))
        
        # Check if item already exists in cart
        cart_item, created = Cart.objects.get_or_create(
            user_id=user_id,
            product_id=product_id,
            product_attr_id=product_attr_id,
            defaults={
                'user_type': request.data.get('user_type', 'Not-Reg'),
                'qty': qty
            }
        )


        if not created:
            # Update quantity if item already exists
            cart_item.qty += qty
            cart_item.save()
            
        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path="update-quantity")
    def update_quantity(self, request):
        """Update item quantity in cart."""
        user_id = request.data.get('user_id')
        product_attr_id = request.data.get('product_attr')
        qty = int(request.data.get('qty', 1))

        print(user_id, product_attr_id, qty)
        try:
            cart_item = Cart.objects.get(user_id=user_id, product_attr_id=product_attr_id)
            if qty <= 0:
                cart_item.delete()
                return Response({'message': 'Item removed from cart'})
            else:

                product_attr = ProductAttribute.objects.get(id=product_attr_id)
                if product_attr.qty < qty:
                    return Response({
                        "error":"out of stock",
                        "available_stock":product_attr.qty
                    }, status=status.HTTP_400_BAD_REQUEST)


                cart_item.qty = qty
                cart_item.save()
                serializer = CartSerializer(cart_item)
                return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'])
    def clear_cart(self, request):
        """Clear all items from cart."""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        Cart.objects.filter(user_id=user_id).delete()
        return Response({'message': 'Cart cleared successfully'})

    @action(detail=True, methods=["delete"], url_path="remove-item")
    def remove_item(self, request, pk):
        "remove item from cart"

        try:
            cart =  Cart.objects.get(id=pk)
            cart.delete()
            return Response({"message":"item deteled"}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({"error":"Object not found."}, status=status.HTTP_404_NOT_FOUND)

