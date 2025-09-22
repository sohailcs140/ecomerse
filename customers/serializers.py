"""
Customer serializers for the ecommerce application.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer

User = get_user_model()


class CustomerSerializer(serializers.ModelSerializer):
    """
    Customer profile serializer.
    """
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    user_type = serializers.CharField(source='user.user_type', read_only=True)
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id', 'user', 'name', 'mobile', 'address', 'city', 'state', 'zip',
            'company', 'gstin', 'status', 'is_verify', 'is_forgot_password',
            'email', 'username', 'user_type', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at', 'rand_id']


class CustomerProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Customer profile update serializer.
    """
    class Meta:
        model = Customer
        fields = [
            'name', 'mobile', 'address', 'city', 'state', 'zip', 'company', 'gstin'
        ]


class CustomerRegistrationSerializer(serializers.Serializer):
    """
    Customer registration serializer that creates both User and Customer.
    """
    # User fields
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)
    
    # Customer fields
    name = serializers.CharField(max_length=100)
    mobile = serializers.CharField(max_length=15, required=False)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        
        # Check if username already exists
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("Username already exists")
            
        # Check if email already exists
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email already exists")
            
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        
        # Extract customer-specific data
        customer_data = {
            'name': validated_data.pop('name'),
            'mobile': validated_data.pop('mobile', ''),
        }
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type='customer'
        )
        
        # Create customer profile
        customer = Customer.objects.create(
            user=user,
            **customer_data
        )
        
        return customer

    def to_representation(self, instance):
        """Return customer data with user information."""
        return CustomerSerializer(instance).data
