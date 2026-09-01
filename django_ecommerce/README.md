# StyleSphere — Premium Printed T-Shirts Studio 👕🔥

StyleSphere is a full-stack, production-ready Django e-commerce platform curated exclusively for **Printed T-Shirts, Anime Graphic Tees, 3D Puff Prints, Oversized Streetwear Drops, and Vintage Acid Wash Tees**.

---

## ⚡ Key Features

1. **Dedicated Printed T-Shirt Catalog**:
   - 6 Curated Categories: Anime & Manga, Oversized & Acid Wash, Cyberpunk & Sci-Fi, Vintage Pop Culture, Minimalist Typography, Marvel & Gaming.
   - Specifications for each Tee: GSM (240-260 GSM French Terry), Print Technology (High-Density Puff Print, DTG, Vintage Screen Print, Holographic), and Fit Type (Oversized Drop Shoulder, Boxy Fit).

2. **Interactive 4-Image Multi-Angle Gallery**:
   - Every product comes equipped with at least 4 distinct views:
     - **Front View**: Chest print / graphic motif
     - **Back View**: High-definition oversized back artwork
     - **Model Aesthetic View**: On-body streetwear styling & drape
     - **Macro Detail View**: High-density ink texture & neckline ribbing
   - Clickable thumbnail carousel with active glow border and modal zoom.

3. **Size Selector & T-Shirt Size Guide**:
   - Sizes S, M, L, XL, XXL with interactive size selector.
   - Built-in modal size guide with chest, length, and shoulder drop measurements.

4. **Dynamic Cart & Checkout Flow**:
   - Size variant support in cart (`f"{product.id}_{size}"`).
   - Free shipping progress bar (unlocked above ₹999).
   - 1-click discount coupons (`FIRST10`, `TEES20`, `STAY5`).
   - Atomic checkout transaction with automated live AWB tracking number generation.

5. **Customer Reviews, Wishlist & Invoicing**:
   - Star ratings and customer review submissions.
   - Live wishlist saved items toggle.
   - Printable HTML/PDF tax invoice with itemized sizes and prices.

---

## 🚀 Quick Setup & Installation

```bash
# 1. Clone or extract the project
cd django_ecommerce

# 2. Install requirements
pip install -r requirements.txt

# 3. Create database tables and apply migrations
python manage.py makemigrations
python manage.py migrate

# 4. Seed the 12 Flagship Printed T-Shirts and Categories
python seed_data.py

# 5. Create superuser (Admin)
python manage.py createsuperuser

# 6. Run local development server
python manage.py runserver
```

Visit the storefront at `http://127.0.0.1:8000/` and the Django Admin at `http://127.0.0.1:8000/admin/`.
