import os
import sys
import urllib.parse
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.translation import override
from core.models import Subscriber


class Command(BaseCommand):
    help = "Send a newsletter edition of 'Morocco Web Tips' to confirmed subscribers in batches."

    def add_arguments(self, parser):
        parser.add_argument('--subject', type=str, required=True, help="Newsletter email subject line")
        parser.add_argument('--body', type=str, help="HTML body content string")
        parser.add_argument('--body-file', type=str, help="Path to an HTML file containing the newsletter body")
        parser.add_argument('--language', type=str, choices=['en', 'fr', 'ar'], help="Send only to subscribers of this language")
        parser.add_argument('--batch-size', type=int, default=50, help="Number of emails per SMTP connection batch (default 50)")
        parser.add_argument('--dry-run', action='store_true', help="Count and display target subscribers without sending emails")

    def handle(self, *args, **options):
        subject = options['subject']
        body_html = options.get('body')
        body_file = options.get('body_file')
        lang_filter = options.get('language')
        batch_size = options.get('batch_size') or 50
        dry_run = options.get('dry_run', False)

        if not body_html and not body_file:
            raise CommandError("You must provide either --body '<p>Content</p>' or --body-file /path/to/newsletter.html")

        if body_file:
            if not os.path.exists(body_file):
                raise CommandError(f"Body file not found: {body_file}")
            with open(body_file, 'r', encoding='utf-8') as f:
                body_html = f.read()

        # Query confirmed subscribers
        qs = Subscriber.objects.filter(is_confirmed=True)
        # Fallback to status='confirmed' if is_confirmed wasn't backfilled
        if not qs.exists():
            qs = Subscriber.objects.filter(status='confirmed')

        if lang_filter:
            qs = qs.filter(language=lang_filter)

        total_subscribers = qs.count()
        self.stdout.write(self.style.NOTICE(f"Targeting {total_subscribers} confirmed subscriber(s)..."))

        if dry_run:
            self.stdout.write(self.style.SUCCESS(f"[DRY-RUN] Would send to {total_subscribers} subscriber(s). Exiting without sending."))
            return

        if total_subscribers == 0:
            self.stdout.write(self.style.WARNING("No confirmed subscribers found. Nothing to send."))
            return

        site_url = getattr(settings, 'SITE_URL', 'https://getnexiro.com').rstrip('/')
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'contact@getnexiro.com')

        total_sent = 0
        total_errors = 0

        # Process in batches
        subscribers_list = list(qs)
        for i in range(0, len(subscribers_list), batch_size):
            batch = subscribers_list[i:i + batch_size]
            messages_to_send = []

            for sub in batch:
                sub_lang = sub.language or 'en'
                unsub_url = f"{site_url}/{sub_lang}/unsubscribe/?email={urllib.parse.quote(sub.email)}"
                
                # Replace subscriber placeholders
                personalized_html = body_html.replace('{unsubscribe_url}', unsub_url)
                personalized_html = personalized_html.replace('{name}', sub.name or '')

                email_ctx = {
                    'subject': subject,
                    'content_html': personalized_html,
                    'content_text': strip_tags(personalized_html),
                    'unsubscribe_url': unsub_url,
                    'site_url': site_url,
                    'language': sub_lang,
                }

                with override(sub_lang):
                    rendered_html = render_to_string('emails/newsletter_broadcast.html', email_ctx)
                    rendered_txt = render_to_string('emails/newsletter_broadcast.txt', email_ctx)

                email_msg = EmailMultiAlternatives(
                    subject=subject,
                    body=rendered_txt,
                    from_email=from_email,
                    to=[sub.email],
                )
                email_msg.attach_alternative(rendered_html, "text/html")
                messages_to_send.append(email_msg)

            # Send batch with a shared SMTP connection
            try:
                connection = get_connection()
                sent_in_batch = connection.send_messages(messages_to_send)
                total_sent += sent_in_batch
                self.stdout.write(f"Batch {i // batch_size + 1}: sent {sent_in_batch}/{len(messages_to_send)} emails.")
            except Exception as e:
                total_errors += len(messages_to_send)
                self.stdout.write(self.style.ERROR(f"Error sending batch {i // batch_size + 1}: {e}"))

        self.stdout.write(self.style.SUCCESS(
            f"Newsletter broadcast finished! Successfully sent: {total_sent}, Errors: {total_errors}."
        ))
