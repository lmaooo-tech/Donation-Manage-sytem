# Implementation Documentation
## Naretoi Charity Donation Management System

## 1. Document Purpose
This document explains how the Naretoi Donation Management System is implemented, what is currently complete, what remains pending, and how to move from development to production safely.

## 2. Project Overview
The system is a Django-based web application for managing donations to Naretoi Charity Organization in Maasailand, Kenya.

Core goals:
- Collect donations through multiple payment channels (PayPal and M-Pesa).
- Track donor information and donation history.
- Segment donations by support categories.
- Provide administration and reporting capabilities.

Current platform stack:
- Backend: Django, Django REST Framework
- Frontend: Django templates, Tailwind CSS (CDN), Font Awesome
- Database: SQLite (development)
- Integrations planned: PayPal Checkout SDK, M-Pesa Daraja API

## 3. Current Implementation Status

### 3.1 Implemented Components
1. Django project scaffolding and configuration
2. Installed apps and middleware setup
3. Core landing and donation pages
4. Donor and donation domain models
5. Admin interfaces for donors, donations, categories, and payment logs
6. Category seeding management command
7. Media/static handling for development

### 3.2 Partially Implemented Components
1. Donation form UI and client-side interactions exist, but server-side processing is not complete.
2. Data structures for payment transaction metadata are in place, but gateway APIs are not integrated.

### 3.3 Not Yet Implemented
1. Live PayPal checkout flow (order create/capture)
2. Live M-Pesa STK push and callback processing
3. Receipt email pipeline
4. Reporting module and dashboards
5. API endpoints for external clients
6. Automated tests (test files exist but are mostly placeholders)

## 4. Repository Structure
Top-level implementation location:
- `Naretoi-project/` contains `manage.py`, apps, templates, static files, and project settings.

Main apps:
- `core/`: public pages and routing
- `donors/`: donor profile model and admin
- `donations/`: categories, donations, payment logs, admin, and seed command
- `payments/`: reserved for payment service integration (currently placeholder)
- `reports/`: reserved for analytics/reporting (currently placeholder)

## 5. Environment and Setup Implementation

### 5.1 Prerequisites
- Python 3.10+
- pip
- Virtual environment tooling

### 5.2 Local Setup Steps (Windows PowerShell)
1. Navigate to project root:
   - `cd "C:\Users\HP\OneDrive\Desktop\DMS code1\Naretoi-project"`
2. Create a virtual environment:
   - `python -m venv .venv`
3. Activate environment:
   - `.\.venv\Scripts\Activate.ps1`
4. Install dependencies:
   - `pip install -r ..\requirements.txt`
5. Apply migrations:
   - `python manage.py migrate`
6. Seed donation categories:
   - `python manage.py seed_categories`
7. Create admin user:
   - `python manage.py createsuperuser`
8. Start server:
   - `python manage.py runserver`

## 6. Configuration Implementation

### 6.1 Key Settings Implemented
- `TIME_ZONE = 'Africa/Nairobi'`
- Static files:
  - `STATIC_URL`, `STATIC_ROOT`, `STATICFILES_DIRS`
- Media files:
  - `MEDIA_URL`, `MEDIA_ROOT`
- Template directory configured at project level
- REST Framework default authentication and permission classes
- Crispy forms configured for Tailwind template pack

### 6.2 Configuration Gaps to Resolve
1. Add secure production environment variable management (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`).
2. Configure production database (PostgreSQL) and connection settings.
3. Add email backend configuration for receipt notifications.
4. Add payment credentials and callback URLs in environment variables.

## 7. Data Model Implementation

### 7.1 Donor Model (`donors.Donor`)
Implemented fields include:
- Identity: full name, email, phone
- Geography: country, city, address
- Classification: donor type, international flag
- Preferences: preferred currency, newsletter subscription
- Stats: donation count, total donated, first/last donation date

Business behavior:
- `update_donation_stats()` recalculates donor totals based on completed donations.
- `is_recurring_donor` property returns true for donation count greater than one.

### 7.2 SupportCategory Model (`donations.SupportCategory`)
Implemented fields include:
- Name, description, icon, image
- Running total for donations
- Active/inactive state

A management command seeds four categories:
- Education Support
- Healthcare Initiatives
- Livelihood Programs
- Access to Water

### 7.3 Donation Model (`donations.Donation`)
Implemented fields include:
- Donor and category links
- Amount, currency, converted KES amount
- Payment method and transaction references
- Gateway-specific fields (PayPal and M-Pesa)
- Status lifecycle (`pending`, `completed`, `failed`, `refunded`)
- Receipt metadata and gateway response payload

Business behavior:
- Auto-generates receipt numbers in format `NAR-YYYY-XXXXX` when completed.

### 7.4 PaymentLog Model (`donations.PaymentLog`)
Implemented for audit/debug with:
- Gateway name
- Action type
- Request/response payloads
- Status code and success flag
- Error details and timestamp

## 8. Web Layer Implementation

### 8.1 URL Routing
- Root URL includes `core.urls`
- Admin available at `/admin/`
- Development media served when `DEBUG=True`

### 8.2 Core Views
- Home view:
  - Lists active support categories
  - Calculates total completed donation amount in KES
  - Calculates unique donor count from completed donations
- Donate view:
  - Renders donation form with category options
  - POST handler currently contains placeholder logic for future processing

### 8.3 Templates
Implemented templates:
- `base.html`: shared layout, navigation, footer, Tailwind and icon setup
- `home.html`: mission and category display with impact metrics
- `donate.html`: multi-step donation UI and frontend interactions

Note:
- `donate.html` currently uses client-side script placeholders and does not submit to a complete backend donation processing flow yet.

## 9. Admin Implementation

### 9.1 Donor Admin
Implemented capabilities:
- Search and filter by donor attributes
- View donor donation metrics
- CSV export action for selected donors

### 9.2 Donation Admin
Implemented capabilities:
- Search by donor and transaction metadata
- Filter by status, payment method, currency, category
- Admin actions to mark selected donations completed/failed

### 9.3 Payment Log Admin
Implemented capabilities:
- Read-only visibility of gateway interactions for audit/debug
- Add/edit disabled to preserve log integrity

## 10. Implementation Risks and Technical Debt
1. Payment workflows are not yet connected to actual APIs.
2. Donation form POST path does not persist donor/donation records yet.
3. No comprehensive automated tests to prevent regressions.
4. Some documentation references differ from current UI/social links and should be harmonized.
5. Project comments indicate Django 6 generation while dependency file targets Django 5.x; version alignment should be verified.

## 11. Implementation Roadmap

### Phase 1: Donation Processing Backend
1. Create Django forms/serializers for donor and donation submission.
2. Validate payloads and persist donor/donation records.
3. Implement currency normalization to KES.
4. Add CSRF-protected POST processing and user feedback states.

Acceptance criteria:
- Submitting the donation form creates donor and pending donation records reliably.

### Phase 2: PayPal Integration
1. Add service layer for order creation and capture.
2. Store PayPal order IDs and payer metadata.
3. Update donation status upon successful capture.
4. Log API requests/responses in `PaymentLog`.

Acceptance criteria:
- Sandbox PayPal flow marks donations completed and records logs.

### Phase 3: M-Pesa Integration
1. Implement OAuth token retrieval and STK push initiation.
2. Build callback endpoint for asynchronous payment confirmations.
3. Update donation status and receipt metadata from callback payload.
4. Add retries and error handling for transient failures.

Acceptance criteria:
- Sandbox M-Pesa flow creates pending donations and confirms completion through callback.

### Phase 4: Receipts and Notifications
1. Generate receipt payload from completed donation data.
2. Configure SMTP/email backend.
3. Send donor confirmation emails and mark `receipt_sent`.
4. Add admin retry action for failed sends.

Acceptance criteria:
- Completed donations trigger successful receipt delivery with tracking.

### Phase 5: Reporting and Observability
1. Implement reports app queries for donation totals by category/date/payment method.
2. Add CSV/XLS exports.
3. Add basic dashboard views and filters.
4. Capture audit-level logs for payment and reporting operations.

Acceptance criteria:
- Admin/report users can retrieve monthly and category-based summaries accurately.

### Phase 6: Test Automation and Release Hardening
1. Add model tests (receipt generation, donor stats updates).
2. Add view tests (home and donation workflow).
3. Add integration tests for payment callback handlers.
4. Configure CI checks (tests + linting).

Acceptance criteria:
- Stable test suite with meaningful coverage and release gating.

## 12. Deployment Implementation Checklist
1. Set `DEBUG=False` in production.
2. Configure secure `SECRET_KEY` and strict `ALLOWED_HOSTS`.
3. Use PostgreSQL and backup policy.
4. Configure static/media hosting strategy.
5. Enforce HTTPS and secure cookies.
6. Add structured application logging.
7. Run migration plan and smoke tests before go-live.

## 13. Operational Commands Reference
- Run development server:
  - `python manage.py runserver`
- Create migrations:
  - `python manage.py makemigrations`
- Apply migrations:
  - `python manage.py migrate`
- Seed support categories:
  - `python manage.py seed_categories`
- Create admin user:
  - `python manage.py createsuperuser`

## 14. Recommended Immediate Next Actions
1. Implement server-side donation form processing in `core.views.donate_view`.
2. Add payment service modules under `payments/` and wire URLs for callbacks.
3. Add initial automated tests for models and core views.
4. Align dependency version strategy and lock framework versions for reproducible deployments.
