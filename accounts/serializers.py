"""
Authentication serializers for the ecommerce application.
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    User registration serializer.
    """
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'user_type', 'mobile']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        # Customer profile will be created automatically by signals
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    User login serializer.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Invalid credentials.')
        else:
            raise serializers.ValidationError('Must include email and password.')


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'user_type', 'mobile', 'date_joined', "first_name", "last_name"]
        read_only_fields = ['id', 'user_type', 'date_joined']
