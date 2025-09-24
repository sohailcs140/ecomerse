"""
Product serializers for the ecommerce application.
"""

from rest_framework import serializers
from .models import Product, ProductAttribute, ProductImage, ProductReview
from core.serializers import BrandSerializer, CategorySerializer, ColorSerializer, SizeSerializer, TaxSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Product image serializer.
    """
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductImageCreateSerializer(serializers.ModelSerializer):
    """
    Product image serializer for creation (without product field).
    """
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductAttributeSerializer(serializers.ModelSerializer):
    """
    Product attribute serializer.
    """
    size_name = serializers.CharField(source='size.size', read_only=True)
    color_name = serializers.CharField(source='color.color', read_only=True)
    discount_percentage = serializers.SerializerMethodField()

    class Meta:
        model = ProductAttribute
        fields = '__all__'

    def get_discount_percentage(self, obj):
        if obj.mrp > obj.price:
            return round(((obj.mrp - obj.price) / obj.mrp) * 100, 2)
        return 0


class ProductAttributeCreateSerializer(serializers.ModelSerializer):
    """
    Product attribute serializer for creation (without product field).
    """
    class Meta:
        model = ProductAttribute
        fields = ['sku', 'attr_image', 'mrp', 'price', 'qty', 'size', 'color']


class ProductReviewSerializer(serializers.ModelSerializer):
    """
    Product review serializer.
    """
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = ProductReview
        fields = '__all__'
        read_only_fields = ['customer', 'added_on']


class ProductListSerializer(serializers.ModelSerializer):
    """
    Product list serializer (minimal data for listing).
    """
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'image', 'slug', 'brand_name', 'category_name',
            'short_desc', 'min_price', 'max_price', 'avg_rating', 'review_count',
            'is_promo', 'is_featured', 'is_discounted', 'is_tranding'
        ]

    def get_min_price(self, obj):
        prices = obj.attributes.values_list('price', flat=True)
        return min(prices) if prices else 0

    def get_max_price(self, obj):
        prices = obj.attributes.values_list('price', flat=True)
        return max(prices) if prices else 0

    def get_avg_rating(self, obj):
        reviews = obj.reviews.filter(status=True)
        if reviews.exists():
            # Convert rating text to numeric for calculation
            rating_map = {'Poor': 1, 'Average': 2, 'Good': 3, 'Very Good': 4, 'Excellent': 5, 'Fantastic': 5}
            total = sum(rating_map.get(review.rating, 3) for review in reviews)
            return round(total / reviews.count(), 1)
        return 0

    def get_review_count(self, obj):
        return obj.reviews.filter(status=True).count()


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Product detail serializer (complete data).
    """
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tax = TaxSerializer(read_only=True)
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_avg_rating(self, obj):
        reviews = obj.reviews.filter(status=True)
        if reviews.exists():
            rating_map = {'Poor': 1, 'Average': 2, 'Good': 3, 'Very Good': 4, 'Excellent': 5, 'Fantastic': 5}
            total = sum(rating_map.get(review.rating, 3) for review in reviews)
            return round(total / reviews.count(), 1)
        return 0

    def get_review_count(self, obj):
        return obj.reviews.filter(status=True).count()


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Product serializer for creation and update with nested images and attributes.
    """
    images = ProductImageCreateSerializer(many=True, required=False)
    attributes = ProductAttributeCreateSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'category', 'name', 'image', 'brand', 'model', 'short_desc', 'desc',
            'keywords', 'technical_specification', 'uses', 'warranty', 'lead_time',
            'tax', 'is_promo', 'is_featured', 'is_discounted', 'is_tranding',
            'status', 'images', 'attributes'
        ]

    def create(self, validated_data):
        # Extract nested data
        images_data = validated_data.pop('images', [])
        attributes_data = validated_data.pop('attributes', [])
        
        # Create the product
        product = Product.objects.create(**validated_data)
        
        # Create associated images
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        
        # Create associated attributes
        for attribute_data in attributes_data:
            ProductAttribute.objects.create(product=product, **attribute_data)
        
        return product

    def update(self, instance, validated_data):
        # Extract nested data
        images_data = validated_data.pop('images', [])
        attributes_data = validated_data.pop('attributes', [])
        
        # Update the product
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Handle images update
        if images_data is not None:
            # Delete existing images if new ones are provided
            instance.images.all().delete()
            # Create new images
            for image_data in images_data:
                ProductImage.objects.create(product=instance, **image_data)
        
        # Handle attributes update
        if attributes_data is not None:
            # Delete existing attributes if new ones are provided
            instance.attributes.all().delete()
            # Create new attributes
            for attribute_data in attributes_data:
                ProductAttribute.objects.create(product=instance, **attribute_data)
        
        return instance
