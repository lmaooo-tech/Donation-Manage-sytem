from django.core.management.base import BaseCommand
from donations.models import SupportCategory


class Command(BaseCommand):
    """
    Management command to seed the database with the 4 support categories.
    Usage: python manage.py seed_categories
    """
    help = 'Seed the database with Naretoi Charity support categories'

    def handle(self, *args, **options):
        """Create the 4 support categories for Naretoi."""
        
        # Define the 4 support categories
        categories_data = [
            {
                'name': 'Education Support',
                'description': 'Supporting education initiatives in Maasailand including school supplies, scholarships, and teacher training programs to improve access to quality education.',
                'icon': 'fa-graduation-cap',
            },
            {
                'name': 'Healthcare Initiatives',
                'description': 'Providing healthcare services and medical supplies to communities in Maasailand, including health camps, immunization programs, and maternal healthcare support.',
                'icon': 'fa-heartbeat',
            },
            {
                'name': 'Livelihood Programs',
                'description': 'Empowering communities through skills training, vocational programs, and microfinance initiatives to generate sustainable income and improve livelihoods.',
                'icon': 'fa-briefcase',
            },
            {
                'name': 'Access to Water',
                'description': 'Building boreholes, water tanks, and purification systems to ensure clean water access for pastoral and farming communities in Maasailand.',
                'icon': 'fa-tint',
            },
        ]

        # Create or update categories
        for category_data in categories_data:
            category, created = SupportCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'icon': category_data['icon'],
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'✗ Already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('\n✓ Support categories seeding completed!')
        )
