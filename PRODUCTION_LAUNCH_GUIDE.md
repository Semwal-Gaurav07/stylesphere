# StyleSphere Production Launch & Deployment Guide 🚀

This guide outlines the exact steps to launch StyleSphere Atelier on a production platform (Render, Railway, Fly.io, or AWS).

---

## 1. Environment Variables Configuration

Create an environment configuration on your hosting provider (e.g. Render Dashboard -> Environment Variables):

| Variable | Description | Example / Recommended Value |
| :--- | :--- | :--- |
| `DEBUG` | Disables debug mode in production | `False` |
| `SECRET_KEY` | Long random cryptographic key | `min-50-characters-random-string` |
| `ALLOWED_HOSTS` | Comma-separated domain names | `your-subdomain.onrender.com,yourdomain.com` |
| `CSRF_TRUSTED_ORIGINS` | Trusted origins for web forms | `https://your-subdomain.onrender.com,https://yourdomain.com` |
| `DATABASE_URL` | Managed PostgreSQL connection string | `postgresql://user:pass@ep-cool-db.us-east-1.aws.neon.tech/stylesphere?sslmode=require` |
| `EMAIL_HOST` | Transactional email SMTP host | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_USE_TLS` | Transport Layer Security | `True` |
| `EMAIL_HOST_USER` | Email account username | `concierge@stylesphere.in` |
| `EMAIL_HOST_PASSWORD`| 16-character Google App Password | `abcd efgh ijkl mnop` (spaces stripped automatically) |
| `DEFAULT_FROM_EMAIL` | Sender display name & address | `Style Sphere Atelier <concierge@stylesphere.in>` |
| `RAZORPAY_KEY_ID` | Live Razorpay API Key ID | `rzp_live_...` |
| `RAZORPAY_KEY_SECRET`| Live Razorpay Key Secret | `...` |
| `RAZORPAY_WEBHOOK_SECRET` | Live Webhook Signature Secret | `...` |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary Cloud Name (Optional) | `stylesphere-atelier` |
| `CLOUDINARY_API_KEY` | Cloudinary API Key | `...` |
| `CLOUDINARY_API_SECRET` | Cloudinary Secret | `...` |

---

## 2. Cloud Database Setup (PostgreSQL)

**Why not SQLite?**
Cloud containers (Render, Railway) use ephemeral filesystems. Any SQLite database will be wiped whenever the server restarts or a new build is deployed.

1. Create a free/starter PostgreSQL database on **Neon** (neon.tech) or **Supabase** (supabase.com).
2. Copy the connection string and assign it to `DATABASE_URL`.
3. The project will automatically connect, enable SSL, and run connection pooling (`conn_max_age=600`).

---

## 3. Persistent Media Storage (Cloudinary or AWS S3)

To ensure customer reviews and uploaded product photography persist across deployments:
1. Sign up for a free Cloudinary account.
2. In your deployment dashboard, add `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET`.
3. StyleSphere will automatically route all uploaded images to Cloudinary via `django-cloudinary-storage`. If omitted, it falls back to local storage.

---

## 4. Razorpay Live Payments & Webhook Setup

1. Switch your Razorpay Dashboard from **Test Mode** to **Live Mode**.
2. Copy your **Key ID** and **Key Secret** into your environment variables.
3. In the Razorpay Dashboard, navigate to **Settings -> Webhooks -> Add New Webhook**:
   - **Webhook URL:** `https://<your-domain>/payment/webhook/`
   - **Secret:** Enter a secret and assign the same value to `RAZORPAY_WEBHOOK_SECRET`.
   - **Active Events:**
     - `order.paid`
     - `payment.captured`
     - `payment.failed`

---

## 5. Render Deployment Commands

* **Build Command:**
  ```bash
  ./build.sh
  ```
* **Start Command:**
  ```bash
  gunicorn ecommerce_project.wsgi:application
  ```

---

## 6. Maintenance & Automated Jobs

### Abandoned Cart / Order Release
If clients abandon checkout after placing orders with unpaid online payment, run the built-in management command to automatically restore reserved inventory:
```bash
python manage.py cleanup_abandoned_orders --minutes 60
```
*You can configure this as a periodic Cron Job (e.g. hourly) on your Render dashboard.*
