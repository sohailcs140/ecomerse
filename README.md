# Ecommerce API

A professional ecommerce REST API built with Django and Django REST Framework, designed for scalability and maintainability.

## Features

- **User Authentication**: JWT-based authentication with custom user model
- **Product Management**: Complete product catalog with categories, brands, attributes, and reviews
- **Order Management**: Full order lifecycle with status tracking and payment integration
- **Shopping Cart**: Session-based cart for registered and guest users
- **Admin Panel**: Django admin interface for backend management
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Filtering & Search**: Advanced product filtering and search capabilities
- **Image Handling**: Product and brand image management
- **Coupon System**: Discount codes with percentage and fixed value options

## Technology Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: JWT with Simple JWT
- **Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Image Processing**: Pillow
- **Environment Management**: python-decouple

## Project Structure

```
ecommerce_api/
├── ecommerce_api/          # Main project settings
│   ├── settings/           # Environment-specific settings
│   │   ├── __init__.py
│   │   ├── base.py        # Base settings
│   │   ├── development.py # Development settings
│   │   └── production.py  # Production settings
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/               # Authentication app
├── core/                   # Core models (brands, categories, etc.)
├── customers/              # Customer management
├── products/               # Product catalog
├── orders/                 # Order and cart management
├── media/                  # User uploaded files
├── static/                 # Static files
├── templates/              # HTML templates
├── requirements/           # Environment-specific requirements
├── docs/                   # Documentation
├── manage.py
└── requirements.txt        # Base requirements
```

## API Endpoints

### Authentication

- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/logout/` - User logout
- `GET /api/v1/auth/profile/` - Get user profile
- `PATCH /api/v1/auth/profile/update/` - Update user profile

### Core

- `GET /api/v1/core/brands/` - List brands
- `GET /api/v1/core/categories/` - List categories
- `GET /api/v1/core/colors/` - List colors
- `GET /api/v1/core/sizes/` - List sizes
- `GET /api/v1/core/banners/` - List home banners
- `POST /api/v1/core/coupons/validate_coupon/` - Validate coupon

### Products

- `GET /api/v1/products/products/` - List products
- `GET /api/v1/products/products/{slug}/` - Product details (by slug)
- `GET /api/v1/products/products/featured/` - Featured products
- `GET /api/v1/products/products/trending/` - Trending products
- `GET /api/v1/products/products/discounted/` - Discounted products
- `GET /api/v1/products/products/search_advanced/` - Advanced search
- `GET /api/v1/products/reviews/` - Product reviews

### Orders

- `GET /api/v1/orders/orders/` - List orders
- `POST /api/v1/orders/orders/` - Create order
- `GET /api/v1/orders/orders/my_orders/` - User's orders
- `GET /api/v1/orders/cart/` - Cart items
- `POST /api/v1/orders/cart/add_item/` - Add to cart
- `POST /api/v1/orders/cart/update_quantity/` - Update cart quantity
- `DELETE /api/v1/orders/cart/clear_cart/` - Clear cart

## Installation & Setup

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Development Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/sohailcs140/ecomerse.git
   cd ecommerce_api
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements/development.txt
   ```

4. **Environment configuration**

   ```bash
   cp env.example .env
   # Edit .env file with your configuration
   ```

5. **Database setup**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   export DJANGO_SETTINGS_MODULE=ecommerce_api.settings.development
   python manage.py runserver
   ```

### Production Setup

1. **Install production dependencies**

   ```bash
   pip install -r requirements/production.txt
   ```

2. **Configure environment variables**

   ```bash
   export DJANGO_SETTINGS_MODULE=ecommerce_api.settings.production
   export SECRET_KEY="your-secret-key"
   export DEBUG=False
   export DB_NAME="your_database"
   export DB_USER="your_user"
   export DB_PASSWORD="your_password"
   # ... other environment variables
   ```

3. **Database setup**

   ```bash
   python manage.py collectstatic --noinput
   python manage.py migrate
   ```

4. **Run with Gunicorn**
   ```bash
   gunicorn ecommerce_api.wsgi:application
   ```

## API Documentation

Once the server is running, you can access the API documentation at:

- **Swagger UI**: http://localhost:8000/api/docs/ - Interactive documentation with organized sections
- **ReDoc**: http://localhost:8000/api/redoc/ - Alternative documentation format
- **OpenAPI Schema**: http://localhost:8000/api/schema/ - Raw OpenAPI 3.0 schema

### Documentation Sections

The API documentation is organized into 6 clear sections:

1. **🔐 Authentication** - User registration, login, logout, and profile management
2. **📦 Products** - Product catalog, reviews, and search functionality
3. **🛒 Orders** - Shopping cart and order management operations
4. **🏷️ Core** - System data like brands, categories, colors, sizes, coupons
5. **👥 Customers** - Customer profile and account management
6. **⚕️ System** - Health checks and API information

## Database Schema

The API is based on the following main entities:

### Core Models

- **Brand**: Product brands with images and status
- **Category**: Hierarchical product categories
- **Color**: Product color variants
- **Size**: Product size variants
- **Tax**: Tax configuration
- **Coupon**: Discount coupons
- **HomeBanner**: Homepage banners
- **OrderStatus**: Order status options

### Product Models

- **Product**: Main product information
- **ProductAttribute**: Product variants (size, color, price, stock)
- **ProductImage**: Additional product images
- **ProductReview**: Customer reviews and ratings

### Order Models

- **Order**: Customer orders with shipping and payment info
- **OrderDetail**: Individual items in orders
- **Cart**: Shopping cart items

### User Models

- **User**: Custom user model with customer/admin types
- **Customer**: Extended customer information
- **Admin**: Admin user information

## Testing

Run the test suite:

```bash
python manage.py test
```

With coverage:

```bash
pytest --cov=.
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.
