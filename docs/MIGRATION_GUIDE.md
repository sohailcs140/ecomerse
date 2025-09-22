# Migration Guide: User-Customer Relationship Update

## Overview

The ecommerce API has been updated to use a cleaner architecture:

- **Removed**: Separate `Admin` model
- **Added**: One-to-one relationship between `User` and `Customer` models
- **Improved**: Single authentication system with extended customer profiles

## Changes Made

### 1. Model Changes

**Before:**

```python
# Separate models
class User(AbstractUser):
    user_type = models.CharField(...)

class Customer(TimestampedModel):
    email = models.EmailField(unique=True)
    password = models.TextField()
    # ... other fields

class Admin(TimestampedModel):
    email = models.EmailField(unique=True)
    password = models.CharField(...)
```

**After:**

```python
# Unified approach
class User(AbstractUser):
    user_type = models.CharField(...)  # 'customer' or 'admin'
    mobile = models.CharField(...)

class Customer(TimestampedModel):
    user = models.OneToOneField(User, ...)  # One-to-one relationship
    name = models.CharField(...)
    mobile = models.CharField(...)
    # ... profile fields only (no email/password)

# Admin model removed - use User with user_type='admin'
```

### 2. Benefits

- **🔐 Single Authentication**: One User model for all authentication
- **👤 Extended Profiles**: Customer model for additional profile data
- **🧹 Cleaner Code**: No duplicate user management
- **📊 Better Relationships**: Proper foreign key relationships in orders/reviews
- **⚡ Auto-Creation**: Customer profiles created automatically via signals

## Migration Steps

### Step 1: Backup Current Database

```bash
# If using SQLite
cp db.sqlite3 db.sqlite3.backup

# If using PostgreSQL
pg_dump your_database > backup.sql
```

### Step 2: Create Fresh Migrations

```bash
# Remove old migration files (if needed)
rm -rf */migrations/00*.py

# Create new migrations
python manage.py makemigrations accounts
python manage.py makemigrations customers
python manage.py makemigrations core
python manage.py makemigrations products
python manage.py makemigrations orders
```

### Step 3: Apply Migrations

```bash
# Apply migrations
python manage.py migrate
```

### Step 4: Create Superuser

```bash
# Create admin user
python manage.py createsuperuser
# Choose user_type='admin' when prompted
```

### Step 5: Populate Initial Data

```bash
# Load your ecom.json data
python manage.py populate_initial_data
```

## API Changes

### Authentication Endpoints (No Changes)

- Registration, login, logout work the same
- JWT tokens work the same

### Customer Endpoints (Updated)

**Before:**

```bash
GET /api/v1/customers/customers/  # Direct customer management
POST /api/v1/customers/admins/    # Separate admin management
```

**After:**

```bash
GET /api/v1/customers/customers/  # Customer profiles (linked to users)
# Admin management through User model in Django admin
```

### Order Endpoints (Improved)

- Orders now properly link to User through Customer profile
- Better relationship integrity
- Same API endpoints, better data structure

## Code Examples

### Creating a Customer User

```python
# Create user (customer profile auto-created by signal)
user = User.objects.create_user(
    username='johndoe',
    email='john@example.com',
    password='securepass123',
    user_type='customer',
    mobile='1234567890'
)

# Access customer profile
customer = user.customer_profile
print(customer.name)  # 'johndoe' (default)
```

### Creating an Admin User

```python
# Create admin user (no customer profile created)
admin = User.objects.create_user(
    username='admin',
    email='admin@example.com',
    password='adminpass123',
    user_type='admin',
    is_staff=True,
    is_superuser=True
)
```

### Accessing Customer Data

```python
# In views/serializers
def get_customer_orders(request):
    customer = request.user.customer_profile
    orders = customer.orders.all()
    return orders
```

## Database Schema Changes

### New Relationships

```sql
-- User table (extended Django User)
accounts_user
├── id (PK)
├── username
├── email
├── password
├── user_type ('customer' | 'admin')
├── mobile
└── ... (other Django User fields)

-- Customer profile table
customers
├── id (PK)
├── user_id (FK -> accounts_user.id) [ONE-TO-ONE]
├── name
├── mobile
├── address
├── city
├── state
└── ... (profile fields)

-- Orders now link properly
orders
├── id (PK)
├── customer_id (FK -> customers.id)
└── ... (order fields)
```

## Testing the Changes

### Run Tests

```bash
# Test the new model structure
python -m pytest tests/unit/test_models.py::TestCustomerModel

# Test API endpoints
python -m pytest tests/api/

# Run all tests
python -m pytest
```

### Verify in Django Admin

1. Go to `/admin/`
2. Check Users section - should show user_type field
3. Check Customers section - should show linked user info
4. No separate Admin model should exist

## Troubleshooting

### Common Issues

1. **Migration Conflicts**

   ```bash
   # Reset migrations if needed
   python manage.py migrate --fake-initial
   ```

2. **Existing Data**

   ```bash
   # If you have existing data, you may need custom migration
   # to transfer data from old Admin model to User model
   ```

3. **Signal Issues**
   ```bash
   # Ensure customers app is properly configured
   # Check customers/apps.py includes signal import
   ```

### Manual Customer Profile Creation

```python
# If signal doesn't work, create manually
from django.contrib.auth import get_user_model
from customers.models import Customer

User = get_user_model()

for user in User.objects.filter(user_type='customer'):
    if not hasattr(user, 'customer_profile'):
        Customer.objects.create(
            user=user,
            name=user.username,
            mobile=user.mobile or ''
        )
```

## Summary

This update provides a much cleaner, more maintainable architecture that follows Django best practices for user management and profile extensions. The one-to-one relationship ensures data integrity while keeping authentication and profile data properly separated.
