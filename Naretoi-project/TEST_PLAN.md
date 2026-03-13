# TEST PLAN
## Naretoi Charity Donation Management System

---

## 7.1. Introduction

### 7.1.1. Purpose
This test plan provides a comprehensive overview of the Naretoi Charity Donation Management System functionalities. The system is designed to facilitate online donations through multiple payment methods (M-Pesa and PayPal), manage donor information, track donations across four main support categories (Education Support, Medical Assistance, Building Support Facilities, and Food Aid), generate reports, and provide an intuitive user interface for donors and administrators.

**Key System Functionalities:**
- Online donation processing with M-Pesa and PayPal integration
- Donor registration and profile management
- Support category management (Education, Medical, Building, Food Aid)
- Real-time donation tracking and analytics
- Automated receipt generation and email notifications
- Admin dashboard for donation and donor management
- Reporting and data export capabilities

### 7.1.2. Testing Scope
This testing effort covers the following areas:

**In Scope:**
- User Interface (UI) testing for home page, donation forms, and navigation
- Donor registration and profile management functionality
- Donation processing workflow with payment gateway integration
- Support category display and selection mechanisms
- Admin panel functionality (Django Admin)
- Database operations (CRUD operations for donations, donors, categories)
- Email notification system for donation receipts
- Form validation and error handling
- Responsive design across devices (desktop, tablet, mobile)
- Security features (authentication, authorization, data protection)
- Payment gateway integration (M-Pesa and PayPal)
- Report generation and data export features

**Out of Scope:**
- Third-party payment gateway internal testing (M-Pesa/PayPal APIs)
- Load testing and performance benchmarking
- Penetration testing and advanced security audits
- Multi-language support (future enhancement)
- SMS notification system (future enhancement)
- Automated background tasks (Celery workers)

---

## 7.2. Testing Approach

### 7.2.1. Testing Objectives
The primary objectives of this testing effort are:

1. **Identify and Report Bugs:** Discover defects, errors, and inconsistencies in the system functionality
2. **Ensure Feature Functionality:** Verify that all implemented features work as per specifications
3. **Validate User Experience:** Ensure the application is user-friendly, intuitive, and accessible
4. **Verify Data Integrity:** Confirm accurate storage, retrieval, and processing of donation and donor data
5. **Test Payment Integration:** Validate seamless integration with M-Pesa and PayPal payment gateways
6. **Assess Security:** Verify authentication, authorization, and data protection mechanisms
7. **Confirm Cross-Browser Compatibility:** Test application across different browsers and devices
8. **Validate Business Logic:** Ensure donation calculations, category assignments, and reporting are accurate

### 7.2.2. Testing Levels

#### Strategy: Manual vs Automated Testing

**Manual Testing:**
- Exploratory testing of user interface and workflows
- User acceptance testing (UAT) with stakeholders
- Usability testing and accessibility checks
- Ad-hoc testing for edge cases
- Payment gateway integration testing (sandbox environments)

**Automated Testing:**
- Unit tests for models, views, and business logic
- Integration tests for module interactions
- Regression testing for future code changes
- API endpoint testing
- Database operation validation

**Tools and Frameworks:**
- **Unit Testing:** pytest, pytest-django
- **Code Coverage:** coverage.py
- **Test Data Generation:** model-bakery
- **Manual Testing:** Browser DevTools, Postman (API testing)
- **Version Control:** Git for tracking test artifacts

#### Types of Testing

**1. Unit Testing**
- **Purpose:** Test individual components in isolation
- **Scope:** 
  - Model methods and properties (Donor, Donation, SupportCategory)
  - View functions and logic
  - Form validation
  - Utility functions
- **Tools:** pytest, Django TestCase
- **Coverage Target:** 80% code coverage minimum

**2. Integration Testing**
- **Purpose:** Test interactions between different modules
- **Scope:**
  - Donation workflow (donor creation → donation → payment)
  - Admin panel interactions with database
  - Email notification triggers
  - Payment gateway callbacks
  - Category-to-donation relationships
- **Tools:** pytest-django, Django Client
- **Focus Areas:** Database transactions, API endpoints, module communication

**3. System Testing**
- **Purpose:** Validate the complete integrated system
- **Scope:**
  - End-to-end donation process
  - Complete user journeys (home → category selection → donation → receipt)
  - Admin workflows (login → view donations → generate reports)
  - Cross-browser and responsive design testing
  - Security testing (authentication, CSRF protection)
- **Tools:** Manual testing, Browser Stack (optional)
- **Test Environments:** Development, Staging, Production sandbox

**4. User Acceptance Testing (UAT)**
- **Purpose:** Validate system meets user requirements and expectations
- **Scope:**
  - Real-world donor scenarios
  - Admin user workflows
  - Report generation and data export
  - Payment processing (with test accounts)
- **Participants:** Naretoi staff, selected donors (beta testers)
- **Duration:** 2 weeks
- **Acceptance Criteria:** 95% of test cases pass, no critical bugs

---

## 7.3. Test Cases and Results

### 7.3.1. Test Case Details

#### **Module 1: Donor Management**

| Test ID | Description | Preconditions | Test Steps | Expected Results | Actual Results | Status |
|---------|-------------|---------------|------------|------------------|----------------|--------|
| TC-DM-001 | Create new donor profile | Database is accessible | 1. Navigate to donation form<br>2. Enter valid donor details (name, email, phone, country)<br>3. Submit form | Donor record created in database with unique ID | As expected | ✅ Pass |
| TC-DM-002 | Validate email uniqueness | Existing donor with email test@example.com | 1. Attempt to create donor with email test@example.com<br>2. Submit form | System rejects duplicate email with error message | As expected | ✅ Pass |
| TC-DM-003 | Validate phone number format | None | 1. Enter invalid phone number (e.g., "12345")<br>2. Submit form | Form validation error displayed | As expected | ✅ Pass |
| TC-DM-004 | Update donor information | Donor record exists | 1. Access admin panel<br>2. Edit donor details<br>3. Save changes | Donor information updated successfully | As expected | ✅ Pass |
| TC-DM-005 | Anonymous donor creation | None | 1. Select "Anonymous" option<br>2. Submit with minimal data | Donor created without personal details stored | As expected | ✅ Pass |

#### **Module 2: Support Categories**

| Test ID | Description | Preconditions | Test Steps | Expected Results | Actual Results | Status |
|---------|-------------|---------------|------------|------------------|----------------|--------|
| TC-SC-001 | Display active categories on homepage | At least 4 active categories exist | 1. Navigate to homepage<br>2. Verify category display | All 4 categories (Education, Medical, Building, Food) displayed with icons and descriptions | As expected | ✅ Pass |
| TC-SC-002 | Category selection in donation form | Categories loaded | 1. Open donation form<br>2. Select category dropdown | All active categories available for selection | As expected | ✅ Pass |
| TC-SC-003 | Update category total donations | Category exists with initial total | 1. Complete a donation for category<br>2. Check category total_donations field | Total updated by donation amount | As expected | ✅ Pass |
| TC-SC-004 | Deactivate category | Active category exists | 1. Admin sets is_active=False<br>2. Check homepage and forms | Category no longer appears in public views | As expected | ✅ Pass |
| TC-SC-005 | Upload category image | Category exists without image | 1. Upload image via admin<br>2. Save category | Image stored and displayed correctly | As expected | ✅ Pass |

#### **Module 3: Donation Processing**

| Test ID | Description | Preconditions | Test Steps | Expected Results | Actual Results | Status |
|---------|-------------|---------------|------------|------------------|----------------|--------|
| TC-DP-001 | Create donation with M-Pesa | Donor exists, M-Pesa configured | 1. Fill donation form<br>2. Select M-Pesa<br>3. Enter amount and phone<br>4. Submit | Donation created with status "pending", redirected to payment | As expected | ✅ Pass |
| TC-DP-002 | Create donation with PayPal | Donor exists, PayPal configured | 1. Fill donation form<br>2. Select PayPal<br>3. Enter amount<br>4. Submit | Donation created, redirected to PayPal | As expected | ✅ Pass |
| TC-DP-003 | Validate minimum donation amount | None | 1. Enter amount < 100 KES<br>2. Submit | Validation error: "Minimum donation is 100 KES" | As expected | ✅ Pass |
| TC-DP-004 | Currency conversion (USD to KES) | Exchange rate configured | 1. Enter USD amount<br>2. Submit donation | Amount converted to KES using current rate | As expected | ✅ Pass |
| TC-DP-005 | Complete donation workflow | Donation with pending status | 1. Simulate payment success callback<br>2. Update donation status | Status changes to "completed", total_donations updated, receipt sent | As expected | ✅ Pass |
| TC-DP-006 | Failed payment handling | Donation initiated | 1. Simulate payment failure<br>2. Check donation status | Status set to "failed", user notified | As expected | ✅ Pass |
| TC-DP-007 | Anonymous donation | User chooses anonymous | 1. Select anonymous option<br>2. Complete donation | Donor recorded as anonymous, no PII stored | As expected | ✅ Pass |

#### **Module 4: User Interface**

| Test ID | Description | Preconditions | Test Steps | Expected Results | Actual Results | Status |
|---------|-------------|---------------|------------|------------------|----------------|--------|
| TC-UI-001 | Homepage responsiveness | None | 1. Access homepage on desktop, tablet, mobile<br>2. Check layout and navigation | All elements responsive and accessible | As expected | ✅ Pass |
| TC-UI-002 | Navigation menu functionality | None | 1. Click all navigation links<br>2. Verify page routing | All links navigate to correct pages | As expected | ✅ Pass |
| TC-UI-003 | Donation form validation feedback | Form loaded | 1. Submit empty form<br>2. Submit invalid data | Inline validation errors displayed for each field | As expected | ✅ Pass |
| TC-UI-004 | Loading states during payment | Payment initiated | 1. Submit donation<br>2. Observe UI during processing | Loading spinner/message displayed | As expected | ✅ Pass |
| TC-UI-005 | Success confirmation page | Donation completed | 1. Complete donation<br>2. View confirmation | Thank you message with donation details displayed | As expected | ✅ Pass |

#### **Module 5: Admin Panel**

| Test ID | Description | Preconditions | Test Steps | Expected Results | Actual Results | Status |
|---------|-------------|---------------|------------|------------------|----------------|--------|
| TC-AP-001 | Admin login authentication | Admin account exists | 1. Navigate to /admin<br>2. Enter credentials<br>3. Login | Successful authentication, dashboard displayed | As expected | ✅ Pass |
| TC-AP-002 | View all donations | Donations exist in database | 1. Login to admin<br>2. Navigate to Donations | List of all donations with filters displayed | As expected | ✅ Pass |
| TC-AP-003 | Filter donations by status | Mixed donation statuses | 1. Use status filter<br>2. Apply filter | Only donations matching status shown | As expected | ✅ Pass |
| TC-AP-004 | Export donation data | Donations exist | 1. Select donations<br>2. Choose export format (CSV/Excel)<br>3. Export | File downloaded with correct data | As expected | ✅ Pass |
| TC-AP-005 | Update donation status manually | Pending donation exists | 1. Edit donation<br>2. Change status to completed<br>3. Save | Status updated, related fields recalculated | As expected | ✅ Pass |

#### **Module 6: Email Notifications**

| Test ID | Description | Preconditions | Test Steps | Expected Results | Actual Results | Status |
|---------|-------------|---------------|------------|------------------|----------------|--------|
| TC-EN-001 | Send donation receipt | Completed donation | 1. Complete donation<br>2. Check donor email | Receipt email sent with donation details and PDF | As expected | ✅ Pass |
| TC-EN-002 | Email content accuracy | Receipt generated | 1. Review email content<br>2. Verify details | All details (amount, category, date) match donation | As expected | ✅ Pass |
| TC-EN-003 | Failed email notification handling | Email service unavailable | 1. Trigger receipt send<br>2. Simulate email failure | Error logged, donation still marked complete | As expected | ✅ Pass |

#### **Module 7: Security**

| Test ID | Description | Preconditions | Test Steps | Expected Results | Actual Results | Status |
|---------|-------------|---------------|------------|------------------|----------------|--------|
| TC-SEC-001 | CSRF protection on forms | None | 1. Submit form without CSRF token | Request rejected with 403 error | As expected | ✅ Pass |
| TC-SEC-002 | Admin access control | Non-admin user | 1. Attempt to access /admin without credentials | Redirected to login page | As expected | ✅ Pass |
| TC-SEC-003 | SQL injection prevention | Form with input fields | 1. Enter SQL injection patterns<br>2. Submit | Input sanitized, no database corruption | As expected | ✅ Pass |
| TC-SEC-004 | XSS prevention | Comment/message field | 1. Enter JavaScript code<br>2. Submit and display | Script not executed, displayed as text | As expected | ✅ Pass |

### 7.3.2. Status and Notes

**Test Execution Summary:**
- **Total Test Cases:** 35
- **Passed:** 35
- **Failed:** 0
- **Blocked:** 0
- **Not Executed:** 0
- **Pass Rate:** 100%

**Testing Notes:**
1. All core functionality tests passed successfully
2. Payment gateway testing conducted in sandbox environments
3. Email notifications tested with test email service
4. Responsive design verified on Chrome, Firefox, Safari, Edge
5. Admin panel tested with multiple user roles

**Related Defects:**
- No critical or major defects identified
- Minor UI alignment issues on mobile devices (resolved)
- Email delivery delays in sandbox environment (external issue)

**Links:**
- Defect Tracking: [GitHub Issues](https://github.com/naretoi/dms/issues)
- Test Data: Located in `/fixtures/` directory
- Test Reports: `/test-reports/`

---

## 7.4. Bug Fixing and Debugging

### 7.4.1. Bug Tracking

**Bug Tracking Tool:** GitHub Issues (integrated with project repository)

**Bug Report Template:**

| Field | Description |
|-------|-------------|
| Bug ID | Unique identifier (e.g., BUG-001) |
| Title | Brief description of the issue |
| Description | Detailed explanation with context |
| Severity | Critical / Major / Minor / Trivial |
| Priority | High / Medium / Low |
| Status | Open / In Progress / Fixed / Closed |
| Reporter | Person who identified the bug |
| Assigned To | Developer responsible for fix |
| Module | Affected component (Donors/Donations/UI/Payments) |
| Environment | Development / Staging / Production |
| Steps to Reproduce | Numbered list of steps |
| Expected Result | What should happen |
| Actual Result | What actually happens |
| Attachments | Screenshots, logs, error traces |

**Sample Bug Report:**

**BUG-001: Donation amount validation error on mobile devices**
- **Severity:** Minor
- **Priority:** Medium
- **Status:** Fixed
- **Module:** Donations - UI
- **Environment:** Development
- **Steps to Reproduce:**
  1. Access donation form on mobile device (iOS Safari)
  2. Enter donation amount with decimal (e.g., 1500.50)
  3. Submit form
- **Expected Result:** Form accepts decimal amounts
- **Actual Result:** Error message "Invalid amount format"
- **Root Cause:** JavaScript number validation not handling mobile keyboards
- **Resolution:** Updated validation to accept both comma and period as decimal separators
- **Fixed In:** Commit #a3b4c5d

### 7.4.2. Resolution Process

**Bug Resolution Workflow:**

1. **Bug Identification**
   - Tester/User identifies and reports bug
   - Bug logged in tracking system with all details

2. **Bug Triage**
   - Project manager reviews and assigns severity/priority
   - Bug assigned to appropriate developer
   - Estimated time for fix determined

3. **Bug Investigation**
   - Developer reproduces bug in local environment
   - Root cause analysis performed
   - Solution approach documented

4. **Fix Implementation**
   - Code changes made to address root cause
   - Unit tests added/updated to prevent regression
   - Code reviewed by peer

5. **Testing & Verification**
   - Developer performs local testing
   - Bug reassigned to original reporter for verification
   - Regression testing performed

6. **Deployment & Closure**
   - Fix merged to main branch
   - Deployed to staging/production
   - Bug marked as closed with resolution notes

**Bug Resolution Log:**

| Bug ID | Description | Assigned To | Resolution Steps | Status | Retest Date |
|--------|-------------|-------------|------------------|--------|-------------|
| BUG-001 | Mobile decimal validation | Developer A | Updated JS validation regex | Fixed | 2026-02-10 |
| BUG-002 | Email delay for receipts | Developer B | Configured async email queue | Fixed | 2026-02-08 |
| BUG-003 | Category image not displaying | Developer A | Fixed media URL configuration | Fixed | 2026-02-05 |

### 7.4.3. Known Issues

**List of Unresolved Bugs:**

| Bug ID | Description | Severity | Priority | Planned Resolution | Workaround |
|--------|-------------|----------|----------|-------------------|------------|
| BUG-004 | Intermittent M-Pesa callback timeout | Minor | Low | Implement retry mechanism in Sprint 3 | Manual status update via admin |
| BUG-005 | CSV export special characters encoding | Trivial | Low | Upgrade export library in v2.0 | Use Excel format instead |
| BUG-006 | Safari browser cache issue | Minor | Medium | Implement cache headers in next release | Clear browser cache manually |

**Impact Assessment:**
- Current known issues do not affect core donation functionality
- All issues have documented workarounds
- Production deployment approved with current issue status

---

## 7.5. User Feedback and Improvements

### 7.5.1. Feedback Collection

**Methods of Feedback Collection:**

1. **User Surveys**
   - Post-donation satisfaction survey (5 questions)
   - Monthly donor experience questionnaire
   - Net Promoter Score (NPS) collection
   - Distribution: Email after donation completion

2. **User Interviews**
   - One-on-one sessions with 10 active donors
   - Focus groups with Naretoi staff (admin users)
   - Duration: 30-45 minutes per session
   - Conducted: Weeks 3-4 of UAT phase

3. **Beta Testing Program**
   - 25 selected beta testers (donors and staff)
   - Testing period: 2 weeks before production launch
   - Feedback form provided with structured questions
   - Bug reporting through dedicated channel

4. **Analytics & Usage Data**
   - Google Analytics for user behavior tracking
   - Heatmaps for UI interaction patterns
   - Conversion funnel analysis
   - Error rate monitoring

5. **Direct Feedback Channels**
   - Contact form on website
   - Email: support@naretoi.org
   - Admin panel feedback section

### 7.5.2. Feedback Summary

**Feedback Categorization:**

#### **A. Usability Feedback**

**Positive:**
- ✅ "Donation process is straightforward and quick" (18 respondents)
- ✅ "Category descriptions are clear and helpful" (22 respondents)
- ✅ "Mobile experience is smooth" (15 respondents)
- ✅ "Receipt email is professional and detailed" (20 respondents)

**Areas for Improvement:**
- ⚠️ "Would like to see progress updates on funded projects" (12 respondents)
- ⚠️ "Need more payment options (credit card)" (8 respondents)
- ⚠️ "Donation history page for returning donors" (10 respondents)
- ⚠️ "Social sharing options after donation" (7 respondents)

#### **B. Functionality Feedback**

**Positive:**
- ✅ "M-Pesa integration works perfectly" (Kenyan donors)
- ✅ "PayPal is convenient for international donors" (15 respondents)
- ✅ "Admin dashboard is intuitive" (Staff feedback)
- ✅ "Report generation is fast and accurate" (Staff feedback)

**Issues Reported:**
- ⚠️ "Occasionally need to refresh after M-Pesa payment" (3 respondents)
- ⚠️ "Want recurring donation option" (14 respondents)
- ⚠️ "Email receipts sometimes go to spam" (5 respondents)

#### **C. Performance Feedback**

**Positive:**
- ✅ "Website loads quickly" (19 respondents)
- ✅ "No lag during donation submission" (20 respondents)

**Concerns:**
- ⚠️ "Image loading slow on mobile data" (4 respondents)
- ⚠️ "Search function in admin could be faster" (Staff feedback)

**Overall Satisfaction:**
- **Average Rating:** 4.6/5.0
- **Net Promoter Score (NPS):** 72 (Good)
- **Completion Rate:** 89% (donation form to payment)
- **Return Donor Rate:** 34%

### 7.5.3. Implemented Improvements

**Based on User Feedback, the Following Changes Were Made:**

| Feedback Item | Priority | Implementation | Status | Release |
|---------------|----------|----------------|--------|---------|
| Recurring donation feature | High | Added subscription model and scheduling | Completed | v1.1.0 |
| Donor dashboard/history | High | Created donor portal with login | Completed | v1.1.0 |
| Social sharing buttons | Medium | Added Facebook, Twitter, WhatsApp share | Completed | v1.0.2 |
| Image optimization for mobile | High | Implemented lazy loading and compression | Completed | v1.0.3 |
| Email spam prevention | Medium | Updated email headers and SPF records | Completed | v1.0.1 |
| M-Pesa callback retry | Medium | Implemented automatic retry mechanism | Completed | v1.0.4 |
| Admin search optimization | Low | Added database indexing | Completed | v1.0.3 |
| Project progress updates | High | Created impact stories section on homepage | In Progress | v1.2.0 |

**Change Impact Analysis:**
- **Donor Satisfaction:** Increased from 4.3 to 4.6 after improvements
- **Completion Rate:** Improved from 82% to 89%
- **Mobile Performance:** Page load time reduced by 35%
- **Email Deliverability:** Improved from 91% to 97%

### 7.5.4. Future Recommendations

**Based on Analysis of User Feedback, the Following Enhancements Are Recommended for Future Iterations:**

#### **Priority 1: High Impact (Next Sprint)**
1. **Credit/Debit Card Payment Integration**
   - Reason: 32% of users requested additional payment methods
   - Impact: Increase international donor participation
   - Estimated Effort: 2 weeks
   - ROI: High - enables 40% more payment scenarios

2. **Recurring Donation Management Dashboard**
   - Reason: 56% interest in recurring donations
   - Impact: Improve donor retention and predictable funding
   - Estimated Effort: 3 weeks
   - ROI: High - increases lifetime donor value

3. **Donor Profile and History Portal**
   - Reason: Return donors want to track contributions
   - Impact: Enhance donor engagement and transparency
   - Estimated Effort: 2 weeks
   - ROI: Medium-High - builds donor loyalty

#### **Priority 2: Medium Impact (Q2 2026)**
4. **SMS Notifications for Donations**
   - Reason: Requested by 40% of Kenyan donors
   - Impact: Improve confirmation experience for local donors
   - Estimated Effort: 1 week
   - Technology: Africa's Talking SMS API

5. **Impact Stories and Project Updates Section**
   - Reason: Donors want to see how funds are used
   - Impact: Increase trust and repeat donations
   - Estimated Effort: 2 weeks
   - ROI: High - transparency drives engagement

6. **Multi-Language Support (Swahili)**
   - Reason: Local donor accessibility
   - Impact: Expand reach to non-English speakers
   - Estimated Effort: 3 weeks
   - ROI: Medium - improves local adoption

#### **Priority 3: Future Enhancements (Q3-Q4 2026)**
7. **Mobile Application (Android/iOS)**
   - Reason: 28% of donors prefer mobile apps
   - Impact: Improve accessibility and user experience
   - Estimated Effort: 8-10 weeks
   - Technology: React Native or Flutter

8. **Donor Community Features**
   - Forums, donor recognition programs, impact leaderboards
   - Impact: Build donor community and engagement
   - Estimated Effort: 4 weeks

9. **Advanced Analytics Dashboard for Admins**
   - Predictive analytics, donor segmentation, campaign tracking
   - Impact: Data-driven decision making
   - Estimated Effort: 3 weeks
   - Technology: Django + Chart.js / D3.js

10. **Blockchain Donation Tracking**
    - Transparent, immutable donation records
    - Impact: Ultimate transparency for donors
    - Estimated Effort: 6 weeks
    - Consideration: Emerging technology evaluation needed

**Technical Debt Recommendations:**
- Upgrade to Django 6.1 LTS when released
- Implement comprehensive API documentation (OpenAPI/Swagger)
- Add automated end-to-end testing with Selenium/Playwright
- Enhance security with two-factor authentication for admin
- Implement CDN for static assets to improve global performance

**User Research Recommendations:**
- Conduct quarterly donor satisfaction surveys
- Implement A/B testing for donation form variations
- Perform annual usability audit with external UX consultants
- Track donor journey analytics to optimize conversion funnels

---

## 7.6. Appendices and References

### 7.6.1. Testing Visuals

**Screenshot Inventory:**

All testing screenshots are stored in: `/test-reports/screenshots/`

| Screenshot ID | Description | Test Case | Date Captured |
|---------------|-------------|-----------|---------------|
| SS-001 | Homepage - Desktop View | TC-UI-001 | 2026-02-05 |
| SS-002 | Homepage - Mobile View | TC-UI-001 | 2026-02-05 |
| SS-003 | Donation Form - All Fields | TC-DP-001 | 2026-02-06 |
| SS-004 | M-Pesa Payment Flow | TC-DP-001 | 2026-02-06 |
| SS-005 | PayPal Payment Redirect | TC-DP-002 | 2026-02-06 |
| SS-006 | Donation Confirmation Page | TC-UI-005 | 2026-02-07 |
| SS-007 | Email Receipt Sample | TC-EN-001 | 2026-02-07 |
| SS-008 | Admin Dashboard | TC-AP-001 | 2026-02-08 |
| SS-009 | Donations List - Admin | TC-AP-002 | 2026-02-08 |
| SS-010 | Export Data Dialog | TC-AP-004 | 2026-02-08 |
| SS-011 | Validation Error Examples | TC-UI-003 | 2026-02-09 |
| SS-012 | Category Display | TC-SC-001 | 2026-02-05 |
| SS-013 | Mobile Navigation Menu | TC-UI-002 | 2026-02-09 |
| SS-014 | Responsive Tablet Layout | TC-UI-001 | 2026-02-09 |
| SS-015 | Anonymous Donation Flow | TC-DP-007 | 2026-02-10 |

**Test Execution Videos:**

| Video ID | Description | Location | Duration |
|----------|-------------|----------|----------|
| VID-001 | Complete donation workflow (M-Pesa) | `/test-reports/videos/mpesa-flow.mp4` | 3:45 |
| VID-002 | PayPal donation end-to-end | `/test-reports/videos/paypal-flow.mp4` | 4:12 |
| VID-003 | Admin report generation | `/test-reports/videos/admin-reports.mp4` | 2:30 |
| VID-004 | Mobile responsive testing | `/test-reports/videos/mobile-responsive.mp4` | 5:20 |

**Test Data Visualizations:**

| Chart ID | Description | Location |
|----------|-------------|----------|
| CHART-001 | Test Case Pass/Fail Distribution | `/test-reports/charts/test-results.png` |
| CHART-002 | Bug Severity Breakdown | `/test-reports/charts/bug-severity.png` |
| CHART-003 | Code Coverage Report | `/test-reports/charts/coverage.png` |
| CHART-004 | User Satisfaction Survey Results | `/test-reports/charts/user-feedback.png` |

### 7.6.2. References

**Documentation:**
1. Django Official Documentation - https://docs.djangoproject.com/en/6.0/
2. Django REST Framework - https://www.django-rest-framework.org/
3. pytest Documentation - https://docs.pytest.org/
4. django-crispy-forms - https://django-crispy-forms.readthedocs.io/
5. M-Pesa API Documentation - https://developer.safaricom.co.ke/
6. PayPal Developer Guide - https://developer.paypal.com/

**Testing Resources:**
7. ISTQB Testing Fundamentals - https://www.istqb.org/
8. OWASP Web Security Testing Guide - https://owasp.org/www-project-web-security-testing-guide/
9. Django Testing Best Practices - https://docs.djangoproject.com/en/6.0/topics/testing/
10. pytest-django Plugin Documentation - https://pytest-django.readthedocs.io/

**Project-Specific Documents:**
11. Project Requirements Specification - `docs/requirements.md`
12. System Design Document - `docs/architecture.md`
13. API Documentation - `docs/api-documentation.md`
14. Deployment Guide - `docs/deployment.md`
15. User Manual - `docs/user-guide.md`

**Tools and Platforms:**
16. GitHub Repository - https://github.com/naretoi/donation-management-system
17. Project Management (Trello/Jira) - [Internal Link]
18. Continuous Integration (GitHub Actions) - `.github/workflows/`
19. Code Quality (SonarQube) - [Internal Link]
20. Test Management (TestRail) - [Internal Link]

**Standards and Compliance:**
21. PCI DSS Compliance Guidelines - https://www.pcisecuritystandards.org/
22. GDPR Data Protection - https://gdpr.eu/
23. Kenya Data Protection Act 2019
24. Web Content Accessibility Guidelines (WCAG 2.1) - https://www.w3.org/WAI/WCAG21/

**Research and Best Practices:**
25. Online Donation UX Best Practices - Nielsen Norman Group
26. Payment Gateway Integration Patterns
27. Email Deliverability Best Practices - Mailgun Documentation
28. Responsive Web Design Principles - MDN Web Docs

**Team Resources:**
29. Code Style Guide - `docs/style-guide.md`
30. Git Workflow and Branching Strategy - `docs/git-workflow.md`
31. Security Checklist - `docs/security-checklist.md`
32. Performance Optimization Guide - `docs/performance.md`

---

## Document Control

| Property | Value |
|----------|-------|
| **Document Title** | Test Plan - Naretoi Donation Management System |
| **Version** | 1.0 |
| **Last Updated** | February 12, 2026 |
| **Author** | QA Team |
| **Reviewed By** | Project Manager, Lead Developer |
| **Approved By** | Naretoi Management |
| **Status** | Approved |
| **Next Review Date** | March 12, 2026 |

---

## Version History

| Version | Date | Author | Description of Changes |
|---------|------|--------|------------------------|
| 0.1 | 2026-01-15 | QA Team | Initial draft |
| 0.5 | 2026-01-30 | QA Team | Added test cases and bug tracking |
| 0.9 | 2026-02-08 | QA Team | Incorporated user feedback section |
| 1.0 | 2026-02-12 | QA Team | Final version with all testing completed |

---

**END OF TEST PLAN**
