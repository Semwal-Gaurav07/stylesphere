# StyleSphere Atelier — Luxury Heavyweight Streetwear & Archival Studio 👕✨

StyleSphere Atelier is an end-to-end, production-grade Django e-commerce platform curated exclusively for **Luxury Streetwear Drops, 240+ GSM French Terry Cotton, 3D High-Density Puff Prints, and Archival Graphic Collections**.

Live Deployment: [https://stylesphere-store.onrender.com/](https://stylesphere-store.onrender.com/)

---

## 💎 Core Architecture & Features

### 1. Luxury Front-End & Sensory Design
* **Cinematic Editorial Layout:** High-contrast obsidian dark palette, typography pairing (*Cinzel*, *Cormorant Garamond*, *Plus Jakarta Sans*), and breathing whitespace.
* **Responsive 2-Column Mobile Grid:** Clean 2-product side-by-side display on mobile viewports (`grid-cols-2`) scaling to 3 columns on desktop.
* **Tactile Audio Branding (Web Audio API):** Native browser synthesizer producing acoustic micro-clicks on size selection and chime feedback (toggleable via `SFX: ON/OFF`).
* **10x Textile Microscopy Loupe:** Interactive high-resolution inspection tool showcasing French Terry looped weave texture and 0.8mm puff print relief.
* **Silhouette Drape Simulator:** Virtual tailoring fitting room calculating drop-shoulder offset, chest ease, and hemline drop based on client height and build.
* **The Unboxing Ritual:** Physical presentation showcase detailing rigid magnetic boxes, wax-sealed Japanese glassine wrap, and cedarwood scent infusion.

### 2. Exclusive Vaults & Provenance
* **Digital Provenance Vault (`/provenance/`):** Serialized cryptographic ledger generating official Certificates of Authenticity with AWB tracking lookup and QA inspection seals.
* **The Midnight Vault (`/vault/`):** Secret restricted drop area gated by VIP passkey (`STYLE2026` or `ATELIER`) with automatic 11:00 PM – 1:00 AM IST curfew unlock.

### 3. Bulletproof E-Commerce & Inventory
* **Per-Size Inventory Tracking:** Granular stock counters across all standard sizes (`S`, `M`, `L`, `XL`, `XXL`) preventing overselling when specific sizes run out.
* **Atomic Concurrency:** Database-level `F('stock') - quantity` decrements wrapped in transactional rollback to eliminate checkout race conditions.
* **Decimal Currency Precision:** High-precision cart and shipping calculations using Python `Decimal` with standard half-up rounding.
* **Pincode & Logistics Serviceability (`/api/pincode/`):** Real-time Indian 6-digit postal pincode validation, estimated delivery date calculation, and COD verification.
* **1-Click WhatsApp Concierge:** Instant WhatsApp dispatch notifications with pre-formatted customer order summaries.

### 4. Payments & Security Hardening
* **Dual Payment Channels:** Seamless Cash on Delivery (COD) and Razorpay gateway integration.
* **Cryptographic Verification:** Server-side HMAC-SHA256 signature verification and automated webhook handler (`/payment/webhook/`).
* **CSRF & Mobile WebView Protection:** Targeted `CSRFOriginFixMiddleware` supporting in-app browsers (Instagram, WhatsApp WebViews).
* **Secure Authentication:** 3-step password recovery with cryptographically secure 6-digit OTP generation via Python `secrets`.
* **Production Deployment Ready:** Automated WhiteNoise static collection, database flexibility via `dj-database-url` (PostgreSQL / SQLite), and strict security headers (`HSTS`, `X-Content-Type-Options`, `Secure Cookies`).

---

## 📁 Project Structure

```
stylesphere/
├── accounts/               # Auth, Profile, and Secure 6-Digit OTP Recovery
├── api/                    # Django REST Framework viewsets and serializers
├── ecommerce_project/      # Settings, hardened middleware, and root routing
├── media/products/         # Uploaded high-resolution product photography
├── payment/                # Razorpay checkout, signature verification, webhooks
├── static/                 # CSS, JavaScript, icons, and branding assets
├── store/                  # Products, variants, cart, checkout, and luxury vaults
│   ├── management/         # Custom management commands (`seed_catalog`)
│   ├── migrations/         # Database migration history
│   ├── templates/store/    # Editorial HTML templates (Mobile 2-col, Vaults, Loupe)
│   └── utils.py            # Pincode serviceability & WhatsApp alert generator
├── check_user_data.py      # Terminal inspector for registered users & order data
├── build.sh                # Render automated build script
├── requirements.txt        # Production Python dependencies
└── .env.example            # Environment configuration template
```

---

## 🚀 Local Installation & Quickstart

```bash
# 1. Clone repository
git clone https://github.com/semwal-gaurav07/stylesphere.git
cd stylesphere

# 2. Set up virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
python manage.py makemigrations
python manage.py migrate

# 5. Populate initial flagship streetwear catalog
python manage.py seed_catalog

# 6. Create superuser account
python manage.py createsuperuser

# 7. Start development server
python manage.py runserver
```

Storefront: `http://127.0.0.1:8000/`  
Admin Control Panel: `http://127.0.0.1:8000/admin/`  
Executive Analytics: `http://127.0.0.1:8000/admin-analytics/`

---

## 🔒 Environment Configuration

Create a `.env` file in the project root based on `.env.example`:

```ini
SECRET_KEY=your-secure-random-secret-key
DEBUG=False
ALLOWED_HOSTS=stylesphere-store.onrender.com,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://stylesphere-store.onrender.com,http://localhost:8000

# Database (PostgreSQL recommended for production)
DATABASE_URL=sqlite:///db.sqlite3

# Email SMTP
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=concierge@stylesphere.in
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Style Sphere Atelier <concierge@stylesphere.in>

# Razorpay Keys
RAZORPAY_KEY_ID=rzp_live_your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
```

---

## 📄 License
Private Commercial License. Developed by Style Sphere Atelier Inc. All rights reserved.
