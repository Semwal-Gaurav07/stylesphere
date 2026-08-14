# Advanced Django E-Commerce Platform

An enterprise-ready Django e-commerce platform featuring User Authentication, Search & Price Filtering, Stripe & Razorpay Payment Workflows, Order History Tracking, and Django REST Framework (DRF) API Endpoints.

---

## Key Features

1. **User Authentication & Customer Profiles (`accounts/`)**
   - User registration (`/accounts/register/`)
   - Custom login & logout (`/accounts/login/`, `/accounts/logout/`)
   - Profile management with shipping address pre-filling (`/accounts/profile/`)
   - Customer Order History dashboard

2. **Search & Advanced Filtering (`store/`)**
   - Full-text search across product names & descriptions (`?q=term`)
   - Minimum and Maximum price range filtering (`?min_price=10&max_price=200`)
   - Product sorting: Price Low-to-High, Price High-to-Low, Newest First (`?sort=price_asc`)
   - Category navigation sidebar

3. **Payment Processing (`payment/`)**
   - Checkout integration with Stripe & Razorpay workflows (`/payment/process/`)
   - Automated order status updates (`paid = True`) upon completion
   - Payment confirmation & cancellation pages (`/payment/done/`, `/payment/canceled/`)

4. **REST API Endpoints (`api/`)**
   - Built with Django REST Framework (DRF)
   - `/api/products/` - List/Search/Filter products
   - `/api/categories/` - List categories
   - `/api/orders/` - Create orders via REST API

5. **Shopping Cart & Checkout**
   - Session-based cart management
   - Item quantity adjustments & item removal
   - Billing & shipping details auto-populated for logged-in users

---

## Quick Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Seed Sample Products & Download Sample Images
```bash
python seed_data.py
python download_images.py
```

### 4. Create an Admin Superuser
```bash
python manage.py createsuperuser
```

### 5. Start Development Server
```bash
python manage.py runserver
```

---

## Main URL Map
- **Storefront**: `http://127.0.0.1:8000/`
- **Sign In / Login**: `http://127.0.0.1:8000/accounts/login/`
- **Register**: `http://127.0.0.1:8000/accounts/register/`
- **My Profile & Order History**: `http://127.0.0.1:8000/accounts/profile/`
- **Cart**: `http://127.0.0.1:8000/cart/`
- **REST API Browser**: `http://127.0.0.1:8000/api/`
- **Admin Dashboard**: `http://127.0.0.1:8000/admin/`
