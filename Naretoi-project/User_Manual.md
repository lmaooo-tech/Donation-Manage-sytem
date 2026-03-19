User Manual Guide
Naretoi Charity Donation Management System. 
Development of a Unified, Web-Based Donation Management System for the Naretoi Charity Organization. 
Candidate's Name: Josphat Osoi Mereu 
Registration Number: 22/06780 
Submission Date March 2026 
Name of Supervisor: Mercy Mukani 
Name of the course/qualification towards which the project contributes: Bachelor of Science in Applied Computing. 
 
DECLARATION ON ORIGINALITY OF WORK 
I hereby declare that this Project Proposal is my original work and has not been presented for an award at any other institution. Where the work of others has been used, it has been duly acknowledged. 
Candidate Signature: Josphat Osoi M. 
Date: 19/03/2026 
User Manual Guide	1
1. Introduction	2
2. System Overview	2
3. For Donors: Making a Contribution	2
3.1. Accessing the Donation Platform	2
3.2. Choosing a Support Category	3
3.3. Completing the Donation Form	3
3.4. Selecting a Payment Method	3
3.5. Donation Confirmation and Receipt	3
4. For Administrators: Managing the System	4
4.1. Accessing the Admin Panel	4
4.2. Dashboard Overview	4
4.3. Managing Support Categories	4
4.4. Managing Donors	4
4.5. Managing Donations	4
4.6. Reviewing Payment Logs	5
5. System Configuration and Maintenance	5
5.1. Environment Variables	5
5.2. Database Management	5
5.3. Static and Media Files	5
6. Troubleshooting and Support	6
References	6

1. Introduction
Welcome to the User Manual for the Naretoi Charity Donation Management System. This guide is designed to assist both donors and administrators in effectively using the platform. The system facilitates online donations to the Naretoi Charity Organisation, allowing for transparent tracking and management of contributions across various support categories.
2. System Overview
The Naretoi Charity Donation Management System is a web-based application built using Django. Its primary purpose is to streamline the donation process, manage donor information, and provide administrative tools for overseeing charitable activities. The system supports donations through multiple payment channels and categorizes them to ensure funds are directed to specific initiatives.
Key Features:
•Online Donation Processing: Facilitates secure donations via PayPal and M-Pesa (planned integration).
•Donor Management: Allows for the registration and management of donor profiles and their donation history.
•Support Category Management: Organizes donations into distinct categories such as Education Support, Healthcare Initiatives, Livelihood Programs, and Access to Water.
•Real-time Tracking: Provides administrators with tools to track donations and donor activity.
•Automated Receipts: Generates and sends receipts for completed donations (planned).
•Admin Dashboard: Offers a centralized interface for managing all aspects of the system.
3. For Donors: Making a Contribution
This section guides you through the process of making a donation to the Naretoi Charity Organisation.
3.1. Accessing the Donation Platform
To make a donation, navigate to the Naretoi Charity website. The homepage will display an overview of the organization's mission and the various support categories available.
3.2. Choosing a Support Category
On the homepage, you will see a list of active Support Categories
. These categories represent the different areas where your donation can make an impact:
•Education Support: Funds for school supplies, scholarships, and teacher training.
•Healthcare Initiatives: Support for medical services, health camps, and maternal care.
•Livelihood Programs: Investment in skills training, vocational programs, and microfinance.
•Access to Water: Contributions towards building boreholes, water tanks, and purification systems.
Select the category that aligns with your philanthropic goals.
3.3. Completing the Donation Form
Clicking on the
Donate Now button or a specific category will take you to the donation form. Here, you will provide details about your donation:
1.Donation Amount: Enter the amount you wish to donate. The system may have a minimum donation amount (e.g., 100 KES)
.
2.Currency: Select your preferred currency (KES, USD, EUR, GBP).
3.Personal Information: Provide your full name, email address, phone number, country, city, and address. Your email is crucial for receiving the donation receipt.
4.Donor Type: You can choose to donate as an 'Individual', 'Corporate/Organization', or 'Anonymous'
. If you choose 'Anonymous', your personal identifying information will not be stored with the donation.
5.Newsletter Subscription: Opt-in or out of receiving updates from Naretoi Charity.
3.4. Selecting a Payment Method
The system is designed to support two primary payment methods:
•M-Pesa: For local donations within Kenya. You will typically be prompted to enter your M-Pesa phone number to initiate an STK Push on your mobile device
.
•PayPal: For international donations. You will be redirected to the PayPal gateway to complete your transaction securely
.
Follow the on-screen instructions for your chosen payment method to finalize the transaction.
3.5. Donation Confirmation and Receipt
Upon successful completion of your donation, you will be redirected to a confirmation page displaying your donation details. An automated receipt will be sent to the email address you provided (once this feature is fully implemented)
. This receipt will include a unique receipt number (e.g., NAR-YYYY-XXXXX)
.
4. For Administrators: Managing the System
This section provides guidance for administrators on how to manage donors, donations, and system settings through the Django Admin interface.
4.1. Accessing the Admin Panel
To access the administration panel, navigate to /admin/ on your system's URL (e.g., http://localhost:8000/admin/ ). You will need to log in with your administrator credentials. If you haven't created an admin user yet, you can do so using the command python manage.py createsuperuser in your development environment
.
4.2. Dashboard Overview
The admin dashboard provides access to various models and configurations. You will typically see sections for:
•Authentication and Authorization: Manage users and groups.
•Donations: Manage Support Categories, Donations, and Payment Logs.
•Donors: Manage Donor profiles.
4.3. Managing Support Categories
Navigate to the Support Categories section under the Donations app. Here you can:
•View Categories: See a list of all defined support categories.
•Add New Category: Create new categories by providing a name, description, icon, and optional image. You can also set whether the category is active
.
•Edit/Deactivate Categories: Modify existing categories or deactivate them if they are no longer accepting donations. Deactivated categories will not appear on the public donation forms
.
4.4. Managing Donors
Under the Donors app, select Donors to manage donor profiles. Here you can:
•View Donors: See a list of all registered donors, including their contact information and donation statistics.
•Search and Filter: Use the search bar and filters to find specific donors by name, email, or country
.
•Edit Donor Information: Update donor details such as contact information or preferences.
•Export Donors: Export selected donor data to a CSV file
.
4.5. Managing Donations
Under the Donations app, select Donations to manage individual donation records. Here you can:
•View Donations: See a list of all donations, including pending, completed, and failed transactions.
•Search and Filter: Filter donations by status, payment method, currency, or support category
.
•Update Donation Status: Manually change the status of a donation (e.g., from 'pending' to 'completed' if a payment was confirmed offline)
.
•View Payment Details: Access detailed payment information, including transaction IDs and gateway responses.
4.6. Reviewing Payment Logs
The Payment Logs section (under Donations) provides a read-only record of all interactions with payment gateways. This is crucial for auditing and debugging payment-related issues
. You can view:
•Gateway: Which payment gateway was used (PayPal or M-Pesa).
•Action: The specific action performed (e.g., 'create_order', 'stk_push', 'callback').
•Payloads: The request and response data exchanged with the payment gateway.
•Status: The success or failure of the operation, along with any error messages.
5. System Configuration and Maintenance
5.1. Environment Variables
Key system settings are managed through environment variables, typically defined in a .env file. These include sensitive information like SECRET_KEY, PAYPAL_CLIENT_ID, MPESA_CONSUMER_KEY, and database credentials
. It is critical to manage these securely, especially in production environments.
5.2. Database Management
The system uses a database to store all its data. For development, SQLite is used, but PostgreSQL is recommended for production environments
.
•Migrations: Whenever changes are made to the data models, database migrations need to be applied using python manage.py makemigrations and python manage.py migrate
.
•Seeding Data: Initial data, such as the default support categories, can be populated using management commands like python manage.py seed_categories
.
5.3. Static and Media Files
•Static Files: These are files like CSS, JavaScript, and images that are part of the application itself. In development, they are served directly, but in production, they should be collected and served efficiently
.
•Media Files: These are user-uploaded files, such as category images. The system is configured to handle their storage and serving
.
6. Troubleshooting and Support
If you encounter any issues or have questions, please refer to the project documentation or contact the system administrator. Common issues might include:
•Payment Failures: Check the Payment Logs in the admin panel for detailed error messages from the payment gateways.
•Missing Data: Ensure that all necessary management commands (e.g., seed_categories) have been run.
•Display Issues: Verify that static files are being served correctly and that the browser cache is cleared.
References
1. Implementation Documentation 1.pdf - Internal project documentation detailing system implementation.
2. Naretoi_Test_Plan.docx - Internal project documentation outlining test cases and expected functionalities.

