"""
Custom postprocessing hooks for Swagger documentation.
"""


def custom_postprocessing_hook(result, generator, request, public):
    """
    Custom postprocessing hook to properly tag API endpoints.
    """
    
    # Define URL pattern to tag mappings
    url_tag_mapping = {
        # Authentication endpoints
        '/api/v1/auth/': 'Authentication',
        
        # Product endpoints
        '/api/v1/products/products/': 'Products',
        '/api/v1/products/reviews/': 'Products',
        '/api/v1/products/attributes/': 'Products',
        
        # Order endpoints
        '/api/v1/orders/orders/': 'Orders',
        '/api/v1/orders/cart/': 'Orders',
        
        # Core endpoints
        '/api/v1/core/brands/': 'Core',
        '/api/v1/core/categories/': 'Core',
        '/api/v1/core/colors/': 'Core',
        '/api/v1/core/sizes/': 'Core',
        '/api/v1/core/taxes/': 'Core',
        '/api/v1/core/coupons/': 'Core',
        '/api/v1/core/banners/': 'Core',
        '/api/v1/core/order-status/': 'Core',
        
        # Customer endpoints
        '/api/v1/customers/customers/': 'Customers',
        '/api/v1/customers/admins/': 'Customers',
        
        # System endpoints
        '/health/': 'System',
        '/': 'System',
    }
    
    # Process each path in the OpenAPI schema
    paths = result.get('paths', {})
    
    for path, path_item in paths.items():
        # Determine the appropriate tag for this path
        tag = None
        
        # Find the best matching tag based on URL pattern
        for url_pattern, tag_name in url_tag_mapping.items():
            if path.startswith(url_pattern):
                tag = tag_name
                break
        
        # If no specific mapping found, try to infer from URL structure
        if not tag:
            if '/api/v1/auth/' in path:
                tag = 'Authentication'
            elif '/api/v1/products/' in path:
                tag = 'Products'
            elif '/api/v1/orders/' in path:
                tag = 'Orders'
            elif '/api/v1/core/' in path:
                tag = 'Core'
            elif '/api/v1/customers/' in path:
                tag = 'Customers'
            else:
                tag = 'System'  # Default for root endpoints
        
        # Apply the tag to all HTTP methods for this path
        for method in ['get', 'post', 'put', 'patch', 'delete', 'options', 'head']:
            if method in path_item:
                operation = path_item[method]
                # Replace existing tags with our custom tag
                operation['tags'] = [tag]
    
    return result
