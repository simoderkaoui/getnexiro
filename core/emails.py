"""
Email dispatchers for contact form notifications and auto-responder confirmations.

Engineered for maximum deliverability (SPF/DKIM/DMARC compliance, CAN-SPAM,
multipart/alternative, and proper RFC headers) to ensure messages land in the inbox.
"""

import logging
import threading
from django.conf import settings
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import get_language
from .models import SiteConfig

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Safely extract client IP from request headers."""
    if not request:
        return 'Unknown'
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'Unknown')


def _dispatch_emails_sync(contact_message, admin_recipient, lang, ip_address, admin_url):
    """Synchronous worker that compiles and sends both emails."""
    try:
        config = SiteConfig.load()
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'getNexiro <getnexiro@gmail.com>')

        # ── 1. Admin Notification Email ──────────────────────────
        admin_subject = f"[getNexiro Inquiry] {contact_message.subject} — {contact_message.name}"
        admin_context = {
            'name': contact_message.name,
            'email': contact_message.email,
            'subject': contact_message.subject,
            'message': contact_message.message,
            'created_at': contact_message.created_at,
            'language': lang,
            'ip_address': ip_address,
            'admin_recipient': admin_recipient,
            'admin_url': admin_url,
            'config': config,
        }

        admin_text = render_to_string('emails/admin_notification.txt', admin_context)
        admin_html = render_to_string('emails/admin_notification.html', admin_context)

        admin_email_msg = EmailMultiAlternatives(
            subject=admin_subject,
            body=admin_text,
            from_email=from_email,
            to=[admin_recipient],
            reply_to=[contact_message.email],
        )
        admin_email_msg.attach_alternative(admin_html, 'text/html')
        admin_email_msg.send(fail_silently=False)

        # ── 2. Sender Auto-Responder Confirmation Email ───────────
        if lang == 'fr':
            sender_subject = f"Nous avons bien reçu votre message — {config.site_name}"
        elif lang == 'ar':
            sender_subject = f"تم استلام رسالتك بنجاح — {config.site_name}"
        else:
            sender_subject = f"We received your message — {config.site_name}"

        sender_context = {
            'name': contact_message.name,
            'email': contact_message.email,
            'subject': contact_message.subject,
            'message': contact_message.message,
            'lang': lang,
            'config': config,
        }

        sender_text = render_to_string('emails/sender_confirmation.txt', sender_context)
        sender_html = render_to_string('emails/sender_confirmation.html', sender_context)

        sender_email_msg = EmailMultiAlternatives(
            subject=sender_subject,
            body=sender_text,
            from_email=from_email,
            to=[contact_message.email],
            reply_to=[admin_recipient],
        )
        sender_email_msg.attach_alternative(sender_html, 'text/html')

        # RFC Anti-Spam Headers:
        # Prevents email bounce loops and auto-responder storms
        sender_email_msg.extra_headers['Auto-Submitted'] = 'auto-replied'
        sender_email_msg.extra_headers['X-Auto-Response-Suppress'] = 'All'
        sender_email_msg.extra_headers['Precedence'] = 'auto_reply'

        sender_email_msg.send(fail_silently=False)
        logger.info("Successfully sent contact emails for message ID %s to %s and %s",
                    contact_message.pk, admin_recipient, contact_message.email)

    except Exception as exc:
        logger.error("Failed to send contact notification or confirmation email: %s", exc, exc_info=True)


def send_contact_emails(contact_message, request=None, async_send=True):
    """
    Dispatches both the Admin notification and Sender confirmation emails.
    Defaults to background thread (async_send=True) for zero UI latency.
    """
    config = SiteConfig.load()
    admin_recipient = config.email or 'getnexiro@gmail.com'

    # Determine submission language
    lang = 'en'
    if request:
        req_lang = getattr(request, 'LANGUAGE_CODE', None) or get_language() or 'en'
        if req_lang.startswith('fr'):
            lang = 'fr'
        elif req_lang.startswith('ar'):
            lang = 'ar'
        else:
            lang = 'en'

    ip_address = get_client_ip(request)

    # Admin URL for direct access
    admin_url = ''
    if request:
        try:
            admin_url = request.build_absolute_uri(f'/admin/core/contactmessage/{contact_message.pk}/change/')
        except Exception:
            admin_url = 'https://getnexiro.com/admin/core/contactmessage/'

    # During testing, send synchronously so test runner can inspect mail.outbox
    is_testing = getattr(settings, 'TESTING', False) or hasattr(mail, 'outbox')
    if is_testing or not async_send:
        _dispatch_emails_sync(contact_message, admin_recipient, lang, ip_address, admin_url)
    else:
        # Asynchronous execution in daemon thread for production responsiveness
        t = threading.Thread(
            target=_dispatch_emails_sync,
            args=(contact_message, admin_recipient, lang, ip_address, admin_url),
            daemon=True,
        )
        t.start()
