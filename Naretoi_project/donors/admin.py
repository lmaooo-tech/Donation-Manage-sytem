from django.contrib import admin
from .models import Donor


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    """
    Admin interface for Donors.
    Shows donor info, donation stats, and contact details.
    """
    list_display = [
        'full_name', 
        'email', 
        'country', 
        'donor_type',
        'donation_count',
        'total_donations',
        'last_donation_date'
    ]
    list_filter = [
        'donor_type', 
        'is_international', 
        'country', 
        'newsletter_subscription',
        'created_at'
    ]
    search_fields = [
        'full_name', 
        'email', 
        'phone_number', 
        'city'
    ]
    readonly_fields = [
        'total_donations',
        'donation_count',
        'first_donation_date',
        'last_donation_date',
        'created_at',
        'updated_at'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone_number')
        }),
        ('Address', {
            'fields': ('country', 'city', 'address')
        }),
        ('Classification', {
            'fields': ('donor_type', 'is_international', 'preferred_currency')
        }),
        ('Preferences', {
            'fields': ('newsletter_subscription',)
        }),
        ('Donation Statistics', {
            'fields': (
                'donation_count',
                'total_donations',
                'first_donation_date',
                'last_donation_date'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['export_to_csv']
    
    def export_to_csv(self, request, queryset):
        """Admin action to export donors to CSV."""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="donors.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Full Name', 'Email', 'Phone', 'Country', 'City',
            'Donor Type', 'Total Donations (KES)', 'Donation Count',
            'Last Donation Date'
        ])
        
        for donor in queryset:
            writer.writerow([
                donor.full_name,
                donor.email,
                str(donor.phone_number) if donor.phone_number else '',
                donor.country.name,
                donor.city,
                donor.get_donor_type_display(),
                donor.total_donations,
                donor.donation_count,
                donor.last_donation_date.strftime('%Y-%m-%d') if donor.last_donation_date else ''
            ])
        
        return response
    export_to_csv.short_description = "Export selected donors to CSV"
