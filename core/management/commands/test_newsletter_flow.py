import sys
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Subscriber, SiteConfig
from core.emails import send_newsletter_subscription_emails


class Command(BaseCommand):
    help = 'Test the full newsletter subscription email flow (both admin alert and subscriber confirmation).'

    def add_arguments(self, parser):
        parser.add_argument(
            'email',
            type=str,
            help='Subscriber email address to test delivery.'
        )
        parser.add_argument(
            '--lang',
            type=str,
            default='en',
            choices=['en', 'fr', 'ar'],
            help='Language for subscriber confirmation email (en, fr, ar).'
        )

    def handle(self, *args, **options):
        test_email = options['email'].strip().lower()
        lang = options['lang']

        self.stdout.write(self.style.MIGRATE_HEADING("\n=== Testing Newsletter Subscription Email Flow ==="))
        self.stdout.write(f"Target Subscriber Email: {test_email}")
        self.stdout.write(f"Language:                {lang}")
        self.stdout.write(f"EMAIL_BACKEND:           {getattr(settings, 'EMAIL_BACKEND', '')}")
        self.stdout.write(f"EMAIL_HOST:              {getattr(settings, 'EMAIL_HOST', '')}")
        self.stdout.write(f"EMAIL_PORT:              {getattr(settings, 'EMAIL_PORT', '')}")
        self.stdout.write(f"EMAIL_USE_SSL:           {getattr(settings, 'EMAIL_USE_SSL', '')}")
        self.stdout.write(f"EMAIL_HOST_USER:         {getattr(settings, 'EMAIL_HOST_USER', '')}")
        self.stdout.write(f"DEFAULT_FROM_EMAIL:      {getattr(settings, 'DEFAULT_FROM_EMAIL', '')}")

        import secrets
        from django.utils import timezone as tz

        # 1. Create or retrieve subscriber
        token = secrets.token_urlsafe(32)
        subscriber, created = Subscriber.objects.get_or_create(
            email__iexact=test_email,
            defaults={
                'email': test_email,
                'source': 'cli_test',
                'language': lang,
                'confirmation_token': token,
                'status': 'pending',
                'is_confirmed': False,
                'consent': True,
            }
        )
        if not created:
            subscriber.confirmation_token = token
            subscriber.token_created_at = tz.now()
            subscriber.language = lang
            subscriber.save(update_fields=['confirmation_token', 'token_created_at', 'language'])
            self.stdout.write(self.style.SUCCESS(f"\n[OK] Refreshed existing Subscriber (ID={subscriber.id}) in database."))
        else:
            self.stdout.write(self.style.SUCCESS(f"\n[OK] Created new Subscriber (ID={subscriber.id}) in database."))

        # 2. Trigger email dispatch synchronously
        self.stdout.write("\nDispatching emails (Admin notification + Subscriber confirmation)...")
        try:
            send_newsletter_subscription_emails(subscriber, request=None, async_send=False)
            self.stdout.write(self.style.SUCCESS("\n[SUCCESS] Newsletter subscription email pipeline finished!"))
            self.stdout.write(f"1. Admin notification sent to contact@getnexiro.com")
            self.stdout.write(f"2. Confirmation & welcome email sent to {test_email}")
            self.stdout.write("\nPlease check your inbox (and spam/junk folder).")
            self.stdout.write("You can also inspect 'email_debug.log' in the project directory for details.\n")
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f"\n[FAIL] Pipeline encountered an exception: {exc}"))
            import traceback
            traceback.print_exc()
