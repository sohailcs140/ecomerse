# API Endpoints Documentation

## Interactive API Documentation

The API documentation is organized into clear sections for easy navigation:

**Swagger UI**: `/api/docs/` - Interactive API documentation with organized sections
**ReDoc**: `/api/redoc/` - Alternative documentation format
**OpenAPI Schema**: `/api/schema/` - Raw OpenAPI 3.0 schema

### Documentation Sections

The Swagger documentation is organized into the following sections:

1. **🔐 Authentication** - User registration, login, logout, and profile management
2. **📦 Products** - Product catalog, reviews, and search functionality
3. **🛒 Orders** - Shopping cart and order management operations
4. **🏷️ Core** - System data like brands, categories, colors, sizes, coupons
5. **👥 Customers** - Customer profile and account management
6. **⚕️ System** - Health checks and API information

## Product Endpoints

### Product Detail by Slug

The product detail endpoint uses **slug** instead of ID for better SEO and user-friendly URLs.

**Endpoint:** `GET /api/v1/products/products/{slug}/`

**Example URLs:**

- `/api/v1/products/products/polo-t-shirt/`
- `/api/v1/products/products/iphone-13-pro/`
- `/api/v1/products/products/nike-air-max/`

**Slug Format:**

- Automatically generated from product name
- Lowercase letters, numbers, and hyphens only
- Unique for each product
- SEO-friendly format

**Example Response:**

```json
{
    "id": 1,
    "name": "Polo T Shirt",
    "slug": "polo-t-shirt",
    "brand": {
        "id": 1,
        "name": "Nike",
        "image": "brands/nike.jpg"
    },
    "category": {
        "id": 1,
        "category_name": "Men",
        "category_slug": "men"
    },
    "short_desc": "100% Original Products...",
    "price_range": {
        "min_price": 749.00,
        "max_price": 999.00
    },
    "attributes": [
        {
            "id": 1,
            "sku": "111",
            "size": "XL",
            "color": "Black",
            "price": 10.00,
            "mrp": 999.00,
            "qty": 5
        }
    ],
    "images": [...],
    "reviews": [...],
    "avg_rating": 4.5,
    "review_count": 10
}
```

### Benefits of Using Slug

1. **SEO Friendly**: Better search engine optimization
2. **User Friendly**: Readable URLs that users can understand
3. **Stable**: URLs don't change even if product ID changes
4. **Memorable**: Easier to share and remember

### Other Product Endpoints

All other product endpoints remain the same:

- `GET /api/v1/products/products/` - List all products
- `GET /api/v1/products/products/featured/` - Featured products
- `GET /api/v1/products/products/trending/` - Trending products
- `GET /api/v1/products/products/discounted/` - Discounted products
- `GET /api/v1/products/products/search_advanced/` - Advanced search

### Frontend Integration

**JavaScript/React Example:**

```javascript
// Instead of using ID
const productId = 123;
const url = `/api/v1/products/products/${productId}/`;

// Use slug for better URLs
const productSlug = "polo-t-shirt";
const url = `/api/v1/products/products/${productSlug}/`;

fetch(url)
  .then((response) => response.json())
  .then((product) => {
    console.log(product.name); // "Polo T Shirt"
  });
```

**URL Patterns:**

```javascript
// Product listing page
/products/

// Product detail page (SEO-friendly)
/products/polo-t-shirt/
/products/iphone-13-pro/
/products/nike-air-max/
```
