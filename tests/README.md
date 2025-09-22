# Test Suite Documentation

This directory contains comprehensive test cases for the ecommerce API project, organized into different categories for better maintainability and clarity.

## Directory Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Pytest configuration and shared fixtures
├── test_runner.py              # Custom test runner utilities
├── README.md                   # This documentation
├── unit/                       # Unit tests
│   ├── __init__.py
│   ├── test_models.py          # Model unit tests
│   ├── test_serializers.py     # Serializer unit tests
│   └── test_slug_functionality.py  # Slug functionality tests
├── api/                        # API endpoint tests
│   ├── __init__.py
│   ├── test_auth_api.py        # Authentication API tests
│   ├── test_core_api.py        # Core API tests
│   ├── test_products_api.py    # Product API tests
│   └── test_orders_api.py      # Order and cart API tests
├── integration/                # Integration tests
│   ├── __init__.py
│   └── test_ecommerce_flow.py  # Complete user flow tests
└── fixtures/                   # Test data fixtures
    ├── __init__.py
    ├── sample_data.json        # Sample test data
    └── ...
```

## Test Categories

### Unit Tests (`tests/unit/`)

- **Purpose**: Test individual components in isolation
- **Coverage**: Models, serializers, utilities, business logic
- **Characteristics**: Fast, isolated, no external dependencies

### API Tests (`tests/api/`)

- **Purpose**: Test API endpoints and HTTP interactions
- **Coverage**: Authentication, CRUD operations, filtering, permissions
- **Characteristics**: Test complete request/response cycle

### Integration Tests (`tests/integration/`)

- **Purpose**: Test complete user workflows and system interactions
- **Coverage**: End-to-end scenarios, cross-module interactions
- **Characteristics**: Comprehensive, realistic user scenarios

## Running Tests

### Prerequisites

```bash
pip install -r requirements/testing.txt
```

### Run All Tests

```bash
# Using pytest (recommended)
pytest

# Using Django test runner
python manage.py test

# Using custom test runner
python run_tests.py
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit/
python run_tests.py tests.unit

# API tests only
pytest tests/api/
python run_tests.py tests.api

# Integration tests only
pytest tests/integration/
python run_tests.py tests.integration
```

### Run Specific Test Files

```bash
# Test specific models
pytest tests/unit/test_models.py

# Test specific API endpoints
pytest tests/api/test_products_api.py

# Test specific class
pytest tests/unit/test_models.py::TestProductModel
```

### Test Options

```bash
# Run with coverage
pytest --cov=.
python run_tests.py --coverage

# Run with verbose output
pytest -v
python run_tests.py --verbose

# Stop on first failure
pytest -x
python run_tests.py --failfast

# Run tests in parallel
pytest -n auto

# Generate HTML coverage report
pytest --cov=. --cov-report=html
```

## Test Configuration

### Pytest Configuration (`pytest.ini`)

- Django settings module
- Coverage settings
- Test discovery patterns
- Custom markers

### Fixtures (`conftest.py`)

Common test fixtures available across all tests:

- `api_client`: Unauthenticated API client
- `authenticated_client`: Authenticated API client
- `admin_client`: Admin authenticated API client
- `user`: Test user instance
- `admin_user`: Admin user instance
- `brand`, `category`, `color`, `size`: Core model instances
- `product`, `product_attribute`: Product model instances
- `customer`: Customer instance

## Writing Tests

### Test Naming Convention

- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

### Example Unit Test

```python
@pytest.mark.django_db
class TestProductModel:
    def test_product_creation(self, category, brand, tax):
        """Test product creation."""
        product = Product.objects.create(
            category=category,
            name='Test Product',
            brand=brand,
            model='Test Model',
            short_desc='Test description',
            tax=tax,
            status=True
        )

        assert product.name == 'Test Product'
        assert str(product) == 'Test Product'
```

### Example API Test

```python
@pytest.mark.django_db
class TestProductsAPI:
    def test_list_products(self, api_client, product):
        """Test listing products."""
        url = reverse('product-list')

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
```

### Example Integration Test

```python
@pytest.mark.django_db
class TestEcommerceFlow:
    def test_complete_shopping_flow(self, api_client, product):
        """Test complete shopping flow."""
        # 1. Register user
        # 2. Browse products
        # 3. Add to cart
        # 4. Place order
        # 5. Verify order
```

## Test Data Management

### Fixtures

Use pytest fixtures for reusable test data:

```python
@pytest.fixture
def product(category, brand, tax):
    return Product.objects.create(...)
```

### Factory Boy (Optional)

For complex test data generation:

```python
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')
    category = factory.SubFactory(CategoryFactory)
```

### JSON Fixtures

Load test data from JSON files:

```bash
python manage.py loaddata tests/fixtures/sample_data.json
```

## Best Practices

### 1. Test Organization

- Group related tests in classes
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

### 2. Database Tests

- Use `@pytest.mark.django_db` for database tests
- Use transactions for test isolation
- Clean up test data automatically

### 3. API Tests

- Test both success and error cases
- Verify response status codes and data
- Test authentication and permissions

### 4. Mocking

- Mock external services
- Use fixtures for consistent test data
- Avoid testing implementation details

### 5. Performance

- Keep tests fast and focused
- Use `pytest-xdist` for parallel execution
- Mock expensive operations

## Coverage Requirements

Target coverage levels:

- **Models**: 95%+ coverage
- **Views/APIs**: 90%+ coverage
- **Serializers**: 90%+ coverage
- **Overall**: 85%+ coverage

## Continuous Integration

Tests are automatically run on:

- Pull requests
- Main branch commits
- Release builds

CI configuration includes:

- Multiple Python versions
- Different Django versions
- Database variations (SQLite, PostgreSQL)

## Troubleshooting

### Common Issues

1. **Database errors**: Ensure `@pytest.mark.django_db` is used
2. **Import errors**: Check Django settings module
3. **Fixture not found**: Verify fixture is in `conftest.py` or imported
4. **Authentication errors**: Use appropriate client fixtures

### Debug Tests

```bash
# Run with pdb debugger
pytest --pdb

# Print output
pytest -s

# Run specific test with verbose output
pytest -v tests/unit/test_models.py::TestProductModel::test_product_creation
```
