from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.conf import settings
from donations.models import SupportCategory, Donation


@require_http_methods(["GET"])
def home_view(request):
    """
    Homepage view - displays organization info and support categories.
    
    Context:
        - categories: All active support categories
        - total_donations: Sum of all completed donations in KES
        - total_donors: Count of unique donors
    """
    categories = SupportCategory.objects.filter(is_active=True)
    
    # Calculate statistics
    completed_donations = Donation.objects.filter(status='completed')
    total_donations = sum(d.amount_in_kes for d in completed_donations)
    total_donors = completed_donations.values('donor').distinct().count()
    
    context = {
        'categories': categories,
        'total_donations': total_donations,
        'total_donors': total_donors,
    }
    
    return render(request, 'home.html', context)


@require_http_methods(["GET", "POST"])
def donate_view(request):
    """
    Donation form view - displays donation form and processes submissions.
    
    GET: Display the donation form with categories
    POST: Process form submission (to be integrated with payment gateways)
    
    Context:
        - categories: All active support categories
    """
    categories = SupportCategory.objects.filter(is_active=True)
    
    if request.method == 'POST':
        # TODO: Process form and handle payment gateway integration
        # For now, this will be handled when we integrate PayPal & M-Pesa
        pass
    
    context = {
        'categories': categories,
        'payment_integration_enabled': settings.PAYMENT_INTEGRATION_ENABLED,
    }
    
    return render(request, 'donate.html', context)
