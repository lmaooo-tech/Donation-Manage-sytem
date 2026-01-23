from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SupportCategory(models.Model):
    """
    Fixed support categories for Naretoi Charity Organization.
    These are the 4 main areas where donations can be directed.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the support category (e.g., Education Support)"
    )
    description = models.TextField(
        help_text="Detailed description of this support area"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon class name (e.g., 'fa-graduation-cap' for FontAwesome)"
    )
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        help_text="Optional image representing this category"
    )
    total_donations = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        help_text="Total amount donated to this category (in KES)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this category is currently accepting donations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Support Category"
        verbose_name_plural = "Support Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Donation(models.Model):
    """
    Records individual donations made through PayPal or M-Pesa.
    Links donor to their donation and tracks payment details.
    """
    PAYMENT_METHOD_CHOICES = [
        ('paypal', 'PayPal'),
        ('mpesa', 'M-Pesa'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    CURRENCY_CHOICES = [
        ('KES', 'Kenyan Shilling'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    ]

    # Donor information (ForeignKey links to Donor model)
    donor = models.ForeignKey(
        'donors.Donor',
        on_delete=models.PROTECT,  # Don't delete donation if donor is deleted
        related_name='donations',
        help_text="The donor who made this donation"
    )

    # Support category
    support_category = models.ForeignKey(
        SupportCategory,
        on_delete=models.PROTECT,
        related_name='donations',
        help_text="Which area this donation supports"
    )

    # Amount details
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Donation amount in original currency"
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='KES',
        help_text="Currency code (KES, USD, EUR, GBP)"
    )
    amount_in_kes = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Donation amount converted to KES for reporting"
    )

    # Payment details
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        help_text="How the donor paid (PayPal or M-Pesa)"
    )
    transaction_id = models.CharField(
        max_length=200,
        unique=True,
        help_text="Unique transaction reference from payment gateway"
    )
    
    # PayPal specific
    paypal_order_id = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="PayPal order ID"
    )
    paypal_payer_email = models.EmailField(
        blank=True,
        null=True,
        help_text="PayPal payer's email"
    )

    # M-Pesa specific
    mpesa_receipt_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="M-Pesa transaction receipt number"
    )
    mpesa_phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Phone number used for M-Pesa payment"
    )

    # Status and tracking
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of this donation"
    )
    payment_response = models.JSONField(
        blank=True,
        null=True,
        help_text="Full payment gateway response (for debugging)"
    )

    # Optional donor message
    message = models.TextField(
        blank=True,
        help_text="Optional message from donor"
    )

    # Timestamps
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="When donation was initiated"
    )
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="When payment was confirmed"
    )

    # Receipt tracking
    receipt_sent = models.BooleanField(
        default=False,
        help_text="Whether receipt email has been sent"
    )
    receipt_number = models.CharField(
        max_length=50,
        blank=True,
        help_text="Unique receipt number"
    )

    class Meta:
        verbose_name = "Donation"
        verbose_name_plural = "Donations"
        ordering = ['-created_at']  # Most recent first
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_method']),
        ]

    def __str__(self):
        return f"{self.donor.full_name} - {self.currency} {self.amount} ({self.status})"

    def save(self, *args, **kwargs):
        """
        Override save method to auto-generate receipt number.
        Format: NAR-YYYY-XXXXX (e.g., NAR-2026-00123)
        """
        if not self.receipt_number and self.status == 'completed':
            # Generate receipt number
            year = timezone.now().year
            last_donation = Donation.objects.filter(
                receipt_number__startswith=f'NAR-{year}'
            ).order_by('-receipt_number').first()
            
            if last_donation:
                last_number = int(last_donation.receipt_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.receipt_number = f'NAR-{year}-{new_number:05d}'
        
        super().save(*args, **kwargs)


class PaymentLog(models.Model):
    """
    Logs all payment gateway interactions for auditing and debugging.
    Stores request/response data from PayPal and M-Pesa.
    """
    GATEWAY_CHOICES = [
        ('paypal', 'PayPal'),
        ('mpesa', 'M-Pesa'),
    ]

    donation = models.ForeignKey(
        Donation,
        on_delete=models.CASCADE,
        related_name='payment_logs',
        null=True,
        blank=True,
        help_text="Associated donation (if created)"
    )
    gateway = models.CharField(
        max_length=10,
        choices=GATEWAY_CHOICES,
        help_text="Which payment gateway was used"
    )
    action = models.CharField(
        max_length=100,
        help_text="Action performed (e.g., 'create_order', 'stk_push', 'callback')"
    )
    request_payload = models.JSONField(
        blank=True,
        null=True,
        help_text="Data sent to payment gateway"
    )
    response_payload = models.JSONField(
        blank=True,
        null=True,
        help_text="Response received from payment gateway"
    )
    status_code = models.IntegerField(
        blank=True,
        null=True,
        help_text="HTTP status code from gateway"
    )
    success = models.BooleanField(
        default=False,
        help_text="Whether the operation was successful"
    )
    error_message = models.TextField(
        blank=True,
        help_text="Error message if operation failed"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Payment Log"
        verbose_name_plural = "Payment Logs"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.gateway} - {self.action} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
