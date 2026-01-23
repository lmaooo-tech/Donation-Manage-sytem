# Naretoi Charity Donation Management

A web-based system for Naretoi Charity Organisation (Maasailand, Kenya) to manage donations across four support categories: Education Support, Healthcare Initiatives, Livelihood Programs, and Access to Water. Payments: PayPal (international) and M-Pesa (local).

## Stack
- Backend: Python 3.10+, Django 5.x, Django REST Framework
- Frontend: HTML + Tailwind CSS (CDN to start; optional local build)
- Database: SQLite for dev, PostgreSQL recommended for prod
- Payments: PayPal Checkout SDK, M-Pesa Daraja API (via direct HTTP calls)
- Extras: crispy-forms + crispy-tailwind, django-environ, Pillow, requests

## Quick Start (Windows, PowerShell)
1) Create and activate a virtual environment
```powershell
python -m venv .venv
./.venv/Scripts/Activate.ps1
```
2) Install dependencies
```powershell
pip install -r requirements.txt
```
3) Create the Django project in the current folder (adds manage.py and naretoi_project/)
```powershell
django-admin startproject naretoi_project .
```
4) Create apps (recommended names)
```powershell
python manage.py startapp core
python manage.py startapp donations
python manage.py startapp donors
python manage.py startapp payments
python manage.py startapp reports
```
5) Configure settings in naretoi_project/settings.py
- Add apps to INSTALLED_APPS: core, donations, donors, payments, reports, rest_framework, crispy_forms, crispy_tailwind, phonenumber_field, django_countries
- Set TIME_ZONE="Africa/Nairobi" and LANGUAGE_CODE="en-us"
- Configure TEMPLATES, STATICFILES_DIRS, MEDIA settings
- Load environment variables (django-environ) from .env

6) Environment variables (.env example)
```dotenv
DEBUG=True
SECRET_KEY=changeme
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite default if omitted)
DATABASE_URL=postgres://user:password@localhost:5432/naretoi

# PayPal
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=your-client-id
PAYPAL_CLIENT_SECRET=your-client-secret

# M-Pesa Daraja
MPESA_ENVIRONMENT=sandbox
MPESA_CONSUMER_KEY=your-consumer-key
MPESA_CONSUMER_SECRET=your-consumer-secret
MPESA_SHORTCODE=your-shortcode
MPESA_PASSKEY=your-passkey
MPESA_CALLBACK_URL=https://example.com/payments/mpesa/callback/

# Email (for receipts)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password
EMAIL_USE_TLS=True
```
7) Apply migrations and create an admin user
```powershell
python manage.py migrate
python manage.py createsuperuser
```
8) Run the dev server
```powershell
python manage.py runserver
```

## Suggested App Responsibilities
- core: home/about pages, base templates, navigation
- donations: SupportCategory (pre-seeded 4 categories), Donation, Receipt
- donors: donor profiles/contact info
- payments: PayPal and M-Pesa integration, webhooks/callbacks, PaymentLog
- reports: dashboard charts, exports (CSV/PDF)

## Tailwind CSS
- Easiest: use CDN in base.html for immediate styling
- If you want a build step later: install Node, run `npm init -y`, `npm install -D tailwindcss postcss autoprefixer`, and generate `tailwind.config.js`/`postcss.config.js`. Compile to static/css/styles.css.

## Payment Notes
- PayPal: use paypalcheckoutsdk, handle order creation + capture, and verify via webhook/callback.
- M-Pesa: use Safaricom Daraja API via HTTPS (requests). Implement STK Push, handle callback URL, store response payloads for auditing.

## Next Steps
- Wire up base templates with Tailwind CDN
- Build models for SupportCategory, Donor, Donation, PaymentLog
- Expose admin for quick data entry/testing
- Implement donation flow (category → amount → donor info → PayPal/M-Pesa → receipt)
- Add dashboard charts (by category, method, period)
