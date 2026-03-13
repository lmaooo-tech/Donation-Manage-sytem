from django.contrib import admin
from .models import SupportCategory, Donation, PaymentLog


@admin.register(SupportCategory)
class SupportCategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Support Categories.
    Shows name, total donations, and active status.
    """
    list_display = ['name', 'total_donations', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'icon')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Statistics', {
            'fields': ('total_donations', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    """
    Admin interface for Donations.
    Shows donor, amount, payment method, and status.
    """
    list_display = [
        'receipt_number', 
        'donor', 
        'support_category', 
        'amount', 
        'currency', 
        'payment_method', 
        'status', 
        'created_at'
    ]
    list_filter = ['status', 'payment_method', 'currency', 'support_category', 'created_at']
    search_fields = [
        'donor__full_name', 
        'donor__email', 
        'transaction_id', 
        'receipt_number',
        'mpesa_receipt_number'
    ]
    readonly_fields = [
        'created_at', 
        'completed_at', 
        'receipt_number', 
        'transaction_id',
        'payment_response'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Donation Details', {
            'fields': ('donor', 'support_category', 'message')
        }),
        ('Amount Information', {
            'fields': ('amount', 'currency', 'amount_in_kes')
        }),
        ('Payment Details', {
            'fields': (
                'payment_method', 
                'status', 
                'transaction_id',
            )
        }),
        ('PayPal Information', {
            'fields': ('paypal_order_id', 'paypal_payer_email'),
            'classes': ('collapse',)
        }),
        ('M-Pesa Information', {
            'fields': ('mpesa_receipt_number', 'mpesa_phone_number'),
            'classes': ('collapse',)
        }),
        ('Receipt Information', {
            'fields': ('receipt_number', 'receipt_sent')
        }),
        ('Technical Details', {
            'fields': ('payment_response', 'created_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_completed', 'mark_as_failed']
    
    def mark_as_completed(self, request, queryset):
        """Admin action to manually mark donations as completed."""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} donation(s) marked as completed.')
    mark_as_completed.short_description = "Mark selected donations as completed"
    
    def mark_as_failed(self, request, queryset):
        """Admin action to manually mark donations as failed."""
        updated = queryset.update(status='failed')
        self.message_user(request, f'{updated} donation(s) marked as failed.')
    mark_as_failed.short_description = "Mark selected donations as failed"


@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    """
    Admin interface for Payment Logs.
    Shows all payment gateway interactions for debugging.
    """
    list_display = ['donation', 'gateway', 'action', 'success', 'created_at']
    list_filter = ['gateway', 'success', 'created_at']
    search_fields = ['donation__transaction_id', 'action', 'error_message']
    readonly_fields = [
        'donation', 
        'gateway', 
        'action', 
        'request_payload', 
        'response_payload',
        'status_code',
        'success',
        'error_message',
        'created_at'
    ]
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        """Prevent manual creation of payment logs."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Make payment logs read-only."""
        return False
