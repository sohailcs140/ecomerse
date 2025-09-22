"""
Customer views for the ecommerce application.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Customer
from .serializers import CustomerSerializer, CustomerRegistrationSerializer, CustomerProfileUpdateSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """
    Customer viewset.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'is_verify']
    search_fields = ['name', 'email', 'mobile']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomerRegistrationSerializer
        return CustomerSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current customer profile."""
        try:
            customer = request.user.customer_profile
            serializer = self.get_serializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer profile not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['patch'])
    def update_profile(self, request):
        """Update current customer profile."""
        try:
            customer = request.user.customer_profile
            serializer = CustomerProfileUpdateSerializer(customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                # Return full customer data
                return Response(CustomerSerializer(customer).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer profile not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def verify_email(self, request, pk=None):
        """Verify customer email."""
        customer = self.get_object()
        customer.is_verify = True
        customer.save()
        return Response({'message': 'Email verified successfully'})


# AdminViewSet removed - using User model with user_type='admin' instead