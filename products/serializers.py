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
    mrp = serializers.DecimalField(max_digits=10, decimal_places=2)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    qty = serializers.IntegerField()
    attr_image = serializers.ImageField(required=False, allow_null=True)
    
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
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'image', 'slug', 'brand_name', 'category_name',
            'short_desc', 'min_price', 'max_price', 'avg_rating', 'review_count',
            'is_promo', 'is_featured', 'is_discounted', 'is_arrival', 'attributes', 'images'
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
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        allow_empty=True,
        write_only=True
    )
    # Remove attributes field from serializer - we'll handle it manually

    class Meta:
        model = Product
        fields = [
            'category', 'name', 'image', 'brand', 'model', 'short_desc', 'desc',
            'keywords', 'technical_specification', 'uses', 'warranty', 'lead_time',
            'tax', 'is_promo', 'is_featured', 'is_discounted', 'is_arrival',
            'status', 'images'
        ]
        read_only_fields = ['slug']

    def parse_attributes_from_form_data(self, request_data):
        """
        Parse attributes from form data with array notation like attributes[0][sku].
        """
        attributes_data = []
        
        # Find all attribute indices
        attribute_indices = set()
        for key in request_data.keys():
            if key.startswith('attributes[') and ']' in key:
                # Extract index from attributes[0][field]
                start = key.find('[') + 1
                end = key.find(']')
                if start > 0 and end > start:
                    try:
                        index = int(key[start:end])
                        attribute_indices.add(index)
                    except ValueError:
                        continue
        
        # Build attributes data for each index
        for index in sorted(attribute_indices):
            attr_data = {}
            
            # Extract all fields for this attribute index
            for key, value in request_data.items():
                if key.startswith(f'attributes[{index}]['):
                    # Extract field name from attributes[0][field]
                    field_start = key.find('][', key.find('[')) + 2
                    field_end = key.rfind(']')
                    if field_start > 1 and field_end > field_start:
                        field_name = key[field_start:field_end]
                        attr_data[field_name] = value
            
            # Only add if we have some data
            if attr_data:
                # Handle empty attr_image
                if 'attr_image' in attr_data and attr_data['attr_image'] == '':
                    attr_data['attr_image'] = None
                
                # Validate the attribute data
                temp_serializer = ProductAttributeCreateSerializer(data=attr_data)
                if temp_serializer.is_valid():
                    attributes_data.append(temp_serializer.validated_data)
                else:
                    print(f"Invalid attribute data for index {index}: {temp_serializer.errors}")
        
        return attributes_data

    def create(self, validated_data):
        # Extract nested data
        images_data = validated_data.pop('images', [])
        
        # Get the original request data to parse attributes
        request_data = self.context.get('request').data if self.context.get('request') else {}
        attributes_data = self.parse_attributes_from_form_data(request_data)
        
        # Create the product
        product = Product.objects.create(**validated_data)
        
        # Create associated images
        for image_file in images_data:
            ProductImage.objects.create(product=product, image=image_file)
        
        # Create associated attributes
        for i, attribute_data in enumerate(attributes_data):
            print(f"Creating attribute {i}: {attribute_data}")
            try:
                ProductAttribute.objects.create(product=product, **attribute_data)
                print(f"Successfully created attribute {i}")
            except Exception as e:
                print(f"Error creating attribute {i}: {e}")
                print(f"Attribute data: {attribute_data}")
        
        return product

    def update(self, instance, validated_data):
        # Extract nested data
        images_data = validated_data.pop('images', [])
        
        # Get the original request data to parse attributes
        request_data = self.context.get('request').data if self.context.get('request') else {}
        attributes_data = self.parse_attributes_from_form_data(request_data)
        
        # Update the product
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Handle images update
        if images_data is not None:
            # Delete existing images if new ones are provided
            instance.images.all().delete()
            # Create new images
            for image_file in images_data:
                ProductImage.objects.create(product=instance, image=image_file)
        
        # Handle attributes update
        if attributes_data is not None:
            # Delete existing attributes if new ones are provided
            instance.attributes.all().delete()
            # Create new attributes
            for attribute_data in attributes_data:
                ProductAttribute.objects.create(product=instance, **attribute_data)
        
        return instance

    def to_representation(self, instance):
        """
        Override to properly handle related objects in response.
        """
        data = super().to_representation(instance)
        
        # Add images and attributes to the response
        try:
            if hasattr(instance, 'images') and instance.pk:
                data['images'] = ProductImageSerializer(instance.images.all(), many=True).data
            else:
                data['images'] = []
        except:
            data['images'] = []
        
        try:
            if hasattr(instance, 'attributes') and instance.pk:
                data['attributes'] = ProductAttributeSerializer(instance.attributes.all(), many=True).data
            else:
                data['attributes'] = []
        except:
            data['attributes'] = []
        
        return data
