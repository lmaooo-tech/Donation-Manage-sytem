from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class Donor(models.Model):
    """
    Stores information about individuals or organizations that donate.
    Can be local (Kenya) or international donors.
    """
    DONOR_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('corporate', 'Corporate/Organization'),
        ('anonymous', 'Anonymous'),
    ]

    # Personal/Organization information
    full_name = models.CharField(
        max_length=200,
        help_text="Full name or organization name"
    )
    email = models.EmailField(
        unique=True,
        help_text="Email address for receipts and communication"
    )
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        help_text="Phone number with country code (e.g., +254712345678)"
    )

    # Address details
    country = CountryField(
        blank_label='Select Country',
        help_text="Donor's country"
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        help_text="City or town"
    )
    address = models.TextField(
        blank=True,
        help_text="Full address (optional)"
    )

    # Donor classification
    donor_type = models.CharField(
        max_length=15,
        choices=DONOR_TYPE_CHOICES,
        default='individual',
        help_text="Type of donor"
    )
    is_international = models.BooleanField(
        default=False,
        help_text="True if donor is outside Kenya"
    )

    # Preferences
    preferred_currency = models.CharField(
        max_length=3,
        default='KES',
        help_text="Preferred donation currency (KES, USD, EUR, GBP)"
    )
    newsletter_subscription = models.BooleanField(
        default=True,
        help_text="Whether donor wants to receive updates"
    )

    # Statistics (auto-calculated)
    total_donations = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        help_text="Total amount donated (in KES)"
    )
    donation_count = models.IntegerField(
        default=0,
        help_text="Number of donations made"
    )
    first_donation_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Date of first donation"
    )
    last_donation_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Date of most recent donation"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Donor"
        verbose_name_plural = "Donors"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['country']),
            models.Index(fields=['-total_donations']),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    def update_donation_stats(self):
        """
        Update donor statistics based on completed donations.
        Called after a successful donation.
        """
        from donations.models import Donation
        
        completed_donations = self.donations.filter(status='completed')
        
        self.donation_count = completed_donations.count()
        self.total_donations = sum(
            donation.amount_in_kes for donation in completed_donations
        )
        
        if completed_donations.exists():
            first = completed_donations.order_by('completed_at').first()
            last = completed_donations.order_by('-completed_at').first()
            self.first_donation_date = first.completed_at
            self.last_donation_date = last.completed_at
        
        self.save()

    @property
    def is_recurring_donor(self):
        """Returns True if donor has made more than one donation."""
        return self.donation_count > 1
