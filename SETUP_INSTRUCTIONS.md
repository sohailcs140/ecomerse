# Setup Instructions for New User-Customer Architecture

## Current Status

✅ **Code Changes Completed:**

- Admin model removed
- User-Customer one-to-one relationship implemented
- Serializers and views updated
- Signals for automatic customer profile creation
- Clean Swagger documentation without decorators

❗ **Database Migration Required:**
The database structure needs to be updated to match the new model architecture.

## Step-by-Step Setup

### 1. Remove Old Database (if exists)

```powershell
# In PowerShell
if (Test-Path db.sqlite3) { Remove-Item db.sqlite3 }
```

### 2. Create Fresh Migrations

```bash
# Create migrations for each app
python manage.py makemigrations accounts
python manage.py makemigrations customers
python manage.py makemigrations core
python manage.py makemigrations products
python manage.py makemigrations orders
```

### 3. Apply Migrations

```bash
# Create the database with new structure
python manage.py migrate
```

### 4. Verify System

```bash
# Check for any issues
python manage.py check
```

### 5. Create Superuser

```bash
# Create admin user
python manage.py createsuperuser
# When prompted for user_type, enter: admin
```

### 6. Start Development Server

```bash
# Start the server
python manage.py runserver
```

### 7. Test the New Architecture

```bash
# Test user registration (creates customer profile automatically)
POST http://127.0.0.1:8000/api/v1/auth/register/
{
    "username": "testcustomer",
    "email": "test@example.com",
    "password": "testpass123",
    "confirm_password": "testpass123",
    "user_type": "customer",
    "mobile": "1234567890"
}
```

## New Architecture Benefits

### 🏗️ **Simplified Structure**

```
Before:                          After:
User ─────────────────────────   User ──────┐
Admin (separate)                 ├── customer_profile (OneToOne)
Customer (separate)              └── user_type ('customer'|'admin')
```

### 🔐 **Authentication Flow**

1. User registers → User created with `user_type='customer'`
2. Signal triggers → Customer profile auto-created
3. User can access profile via `user.customer_profile`
4. Orders/Reviews link through Customer → User

### 📊 **API Endpoints Updated**

- **Authentication**: Same endpoints, better backend
- **Customer Management**: Now properly linked to User
- **Orders**: Better relationship integrity
- **Admin**: Use Django admin with User model

## Troubleshooting

### If Migration Fails

```bash
# Reset migrations if needed
python manage.py migrate --run-syncdb

# Or create migrations individually
python manage.py makemigrations accounts --empty
# Edit migration file manually if needed
```

### If Tests Fail

```bash
# Tests will work after migrations are applied
python -m pytest tests/unit/test_models.py::TestCustomerModel -v
```

### If Customer Profile Not Created

```bash
# Check if signals are working
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.create_user(username='test', email='test@test.com', password='pass', user_type='customer')
>>> print(hasattr(user, 'customer_profile'))  # Should be True
```

## What's Ready to Use

✅ **Clean Code Architecture**

- No redundant Admin model
- Proper User-Customer relationship
- Automatic profile creation

✅ **Professional API Structure**

- 6 organized Swagger sections
- Clean, decorator-free views
- Proper authentication flow

✅ **Comprehensive Testing**

- Updated test fixtures
- User-Customer relationship tests
- API endpoint tests

✅ **Production Ready**

- Environment-specific settings
- Security configurations
- Scalable architecture

Once you complete the migration steps above, your ecommerce API will be ready with the new, cleaner architecture! 🚀
