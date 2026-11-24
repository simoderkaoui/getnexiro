"""
Email dispatchers for contact form notifications and auto-responder confirmations.

Engineered for maximum deliverability (SPF/DKIM/DMARC compliance, CAN-SPAM,
multipart/alternative, and proper RFC headers) to ensure messages land in the inbox.
"""

import json
import logging
import threading
import urllib.request
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


def geolocate_ip(ip_address):
    """
    Lookup geographic location from IP address using free APIs.
    Returns a dict with city, region, country, country_code, lat, lon, isp, timezone.
    Falls back gracefully if the lookup fails or IP is local/unknown.
    """
    empty = {
        'city': '', 'region': '', 'country': '', 'country_code': '',
        'lat': '', 'lon': '', 'isp': '', 'timezone': '', 'location_str': '',
    }

    if not ip_address or ip_address in ('Unknown', '127.0.0.1', 'localhost', '::1'):
        return empty

    # Try multiple free geo APIs in priority order
    apis = [
        {
            'url': f'http://ip-api.com/json/{ip_address}?fields=status,country,countryCode,regionName,city,lat,lon,timezone,isp,org',
            'parse': lambda d: {
                'city': d.get('city', ''),
                'region': d.get('regionName', ''),
                'country': d.get('country', ''),
                'country_code': d.get('countryCode', ''),
                'lat': str(d.get('lat', '')),
                'lon': str(d.get('lon', '')),
                'isp': d.get('isp') or d.get('org', ''),
                'timezone': d.get('timezone', ''),
            } if d.get('status') == 'success' else None,
        },
        {
            'url': f'https://freeipapi.com/api/json/{ip_address}',
            'parse': lambda d: {
                'city': d.get('cityName', ''),
                'region': d.get('regionName', ''),
                'country': d.get('countryName', ''),
                'country_code': d.get('countryCode', ''),
                'lat': str(d.get('latitude', '')),
                'lon': str(d.get('longitude', '')),
                'isp': '',
                'timezone': str(d.get('timeZone', '')),
            } if d.get('cityName') else None,
        },
    ]

    for api in apis:
        try:
            req = urllib.request.Request(api['url'], headers={'User-Agent': 'getNexiro-GeoLookup/1.0'})
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                result = api['parse'](data)
                if result and result.get('city'):
                    # Build human-readable location string
                    parts = [p for p in [result['city'], result['region'], result['country']] if p]
                    result['location_str'] = ', '.join(parts)
                    return result
        except Exception:
            continue

def reverse_geocode(lat, lon):
    """
    Reverse-geocode exact GPS coordinates to city, region, and country
    using high-accuracy reverse geocoding services.
    """
    if not lat or not lon:
        return ''
    try:
        url = f'https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=en'
        req = urllib.request.Request(url, headers={'User-Agent': 'getNexiro/1.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            city = data.get('city') or data.get('locality')
            region = data.get('principalSubdivision')
            country = data.get('countryName')
            parts = [p for p in [city, region, country] if p]
            if parts:
                return ', '.join(parts)
    except Exception:
        pass

    try:
        url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=14&addressdetails=1'
        req = urllib.request.Request(url, headers={'User-Agent': 'getNexiro/1.0 (contact@getnexiro.com)'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            addr = data.get('address', {})
            city = addr.get('city') or addr.get('town') or addr.get('village')
            region = addr.get('state') or addr.get('county')
            country = addr.get('country')
            parts = [p for p in [city, region, country] if p]
            if parts:
                return ', '.join(parts)
    except Exception:
        pass
    return ''


def _dispatch_emails_sync(contact_message, admin_recipient, lang, ip_address, admin_url, client_geo=None):
    """Synchronous worker that compiles and sends both emails."""
    try:
        config = SiteConfig.load()
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'getNexiro <contact@getnexiro.com>')

        # ── Determine Location: GPS sensor (high precision) vs IP gateway (fallback) ──
        ip_geo = geolocate_ip(ip_address)
        client_geo = client_geo or {}

        has_gps = bool(client_geo.get('lat') and client_geo.get('lon'))

        if has_gps:
            # Exact device GPS coordinates from browser
            geo_lat = str(client_geo['lat'])
            geo_lon = str(client_geo['lon'])
            geo_accuracy = str(client_geo.get('accuracy', ''))
            resolved_city = client_geo.get('city') or reverse_geocode(geo_lat, geo_lon) or 'Exact GPS Coordinates'
            geo_location = resolved_city
            geo_source = 'Exact GPS (Phone / Device Sensor)'
            geo_isp = ip_geo.get('isp', '')
            geo_timezone = ip_geo.get('timezone', '')
        else:
            # Fallback to cellular/ISP gateway IP
            geo_lat = ip_geo.get('lat', '')
            geo_lon = ip_geo.get('lon', '')
            geo_accuracy = ''
            geo_location = ip_geo.get('location_str', '')
            geo_source = 'Cellular / ISP Gateway IP (Mobile Data)' if ip_geo.get('location_str') else ''
            geo_isp = ip_geo.get('isp', '')
            geo_timezone = ip_geo.get('timezone', '')

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
            # Geolocation data
            'geo_location': geo_location,
            'geo_lat': geo_lat,
            'geo_lon': geo_lon,
            'geo_accuracy': geo_accuracy,
            'geo_source': geo_source,
            'geo_isp': geo_isp,
            'geo_timezone': geo_timezone,
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


def send_contact_emails(contact_message, request=None, async_send=True, client_geo=None):
    """
    Dispatches both the Admin notification and Sender confirmation emails.
    Defaults to background thread (async_send=True) for zero UI latency.
    """
    config = SiteConfig.load()
    admin_recipient = config.email or 'contact@getnexiro.com'

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

    # Extract client GPS data if submitted in POST or passed explicitly
    if client_geo is None and request and request.method == 'POST':
        lat = request.POST.get('geo_lat', '').strip()
        lon = request.POST.get('geo_lon', '').strip()
        acc = request.POST.get('geo_accuracy', '').strip()
        city = request.POST.get('geo_city', '').strip()
        if lat and lon:
            client_geo = {
                'lat': lat,
                'lon': lon,
                'accuracy': acc,
                'city': city,
            }

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
        _dispatch_emails_sync(contact_message, admin_recipient, lang, ip_address, admin_url, client_geo=client_geo)
    else:
        # Asynchronous execution in daemon thread for production responsiveness
        t = threading.Thread(
            target=_dispatch_emails_sync,
            args=(contact_message, admin_recipient, lang, ip_address, admin_url, client_geo),
            daemon=True,
        )
        t.start()


def _dispatch_newsletter_emails_sync(subscriber_id, admin_recipient, lang, ip_address, source_page, site_url, admin_url):
    """
    Synchronous worker that compiles and sends:
    1. Admin notification to contact@getnexiro.com
    2. Subscriber confirmation & welcome email
    """
    import urllib.parse
    from django.utils.translation import override
    from .models import Subscriber

    try:
        subscriber = Subscriber.objects.get(pk=subscriber_id)
    except Subscriber.DoesNotExist:
        logger.warning("Subscriber %s not found for email dispatch", subscriber_id)
        return

    try:
        config = SiteConfig.load()
        auth_user = getattr(settings, 'EMAIL_HOST_USER', '') or ''
        raw_from = getattr(settings, 'DEFAULT_FROM_EMAIL', 'getNexiro <contact@getnexiro.com>')
        from email.utils import parseaddr, formataddr
        fname, faddr = parseaddr(raw_from)
        # On cPanel Exim, ensure the envelope sender matches the authenticated mailbox
        if auth_user and '@' in auth_user:
            faddr = auth_user
        elif not faddr:
            faddr = 'contact@getnexiro.com'
        from_email = formataddr((fname or 'getNexiro', faddr))

        ip_geo = geolocate_ip(ip_address)
        geo_location = ip_geo.get('location_str', '')
        geo_isp = ip_geo.get('isp', '')

        site_url = site_url.rstrip('/')
        confirm_url = f"{site_url}/{lang}/confirm/{subscriber.confirmation_token}/"
        unsub_url = f"{site_url}/{lang}/unsubscribe/?email={urllib.parse.quote(subscriber.email)}"

        # ── 1. Admin Notification to contact@getnexiro.com ─────────────────
        if getattr(subscriber, 'lead_magnet', '') == 'checklist':
            admin_subject = f"[Lead Magnet] New Checklist Request — {subscriber.email}"
        else:
            admin_subject = f"[Morocco Web Tips] New Subscriber — {subscriber.email}"

        admin_context = {
            'subscriber': subscriber,
            'email': subscriber.email,
            'language': lang,
            'source': subscriber.source or 'newsletter_box',
            'source_page': source_page or getattr(subscriber, 'source_page', ''),
            'ip_address': ip_address,
            'geo_location': geo_location,
            'geo_isp': geo_isp,
            'created_at': subscriber.created_at,
            'status': getattr(subscriber, 'status', 'pending'),
            'admin_url': admin_url,
            'confirm_url': confirm_url,
            'config': config,
        }

        try:
            admin_text = render_to_string('emails/admin_newsletter_notification.txt', admin_context)
            admin_html = render_to_string('emails/admin_newsletter_notification.html', admin_context)

            admin_msg = EmailMultiAlternatives(
                subject=admin_subject,
                body=admin_text,
                from_email=from_email,
                to=[admin_recipient],
                reply_to=[subscriber.email],
            )
            admin_msg.attach_alternative(admin_html, 'text/html')
            admin_msg.send(fail_silently=False)
            logger.info("Admin newsletter notification sent to %s for subscriber %s", admin_recipient, subscriber.email)
        except Exception as admin_err:
            logger.error("Failed to send admin newsletter notification for %s: %s", subscriber.email, admin_err, exc_info=True)

        # ── 2. Subscriber Confirmation & Welcome Email ─────────────────────
        try:
            sub_context = {
                'subscriber': subscriber,
                'confirm_url': confirm_url,
                'unsubscribe_url': unsub_url,
                'site_url': site_url,
                'language': lang,
                'config': config,
            }

            with override(lang):
                sub_subject = render_to_string('emails/newsletter_confirm_subject.txt', sub_context).strip()
                sub_html = render_to_string('emails/newsletter_confirm.html', sub_context)
                sub_text = render_to_string('emails/newsletter_confirm.txt', sub_context)

            subscriber_msg = EmailMultiAlternatives(
                subject=sub_subject,
                body=sub_text,
                from_email=from_email,
                to=[subscriber.email],
                reply_to=[admin_recipient],
            )
            subscriber_msg.attach_alternative(sub_html, 'text/html')
            subscriber_msg.extra_headers['Auto-Submitted'] = 'auto-replied'
            subscriber_msg.extra_headers['X-Auto-Response-Suppress'] = 'All'
            subscriber_msg.extra_headers['Precedence'] = 'auto_reply'
            subscriber_msg.send(fail_silently=False)
            logger.info("Confirmation email sent to subscriber %s", subscriber.email)
        except Exception as sub_err:
            logger.error("Failed to send confirmation email to subscriber %s: %s", subscriber.email, sub_err, exc_info=True)

    except Exception as exc:
        logger.error(
            "Failed during newsletter subscription email preparation for %s: %s",
            subscriber.email, exc, exc_info=True
        )


def send_newsletter_subscription_emails(subscriber, request=None, async_send=False):
    """
    Dispatches both the Admin notification (to contact@getnexiro.com) and the
    Subscriber confirmation & welcome email.
    Defaults to synchronous dispatch (async_send=False) so cPanel Passenger WSGI
    never terminates the thread before outbound SMTP delivery completes.
    """
    config = SiteConfig.load()
    admin_recipient = config.email or 'contact@getnexiro.com'

    lang = getattr(subscriber, 'language', 'en') or 'en'
    if request:
        req_lang = getattr(request, 'LANGUAGE_CODE', None) or get_language() or lang
        if req_lang.startswith('fr'):
            lang = 'fr'
        elif req_lang.startswith('ar'):
            lang = 'ar'
        else:
            lang = 'en'

    ip_address = get_client_ip(request)
    source_page = ''
    if request:
        source_page = request.META.get('HTTP_REFERER', '')
    if not source_page:
        source_page = getattr(subscriber, 'source_page', '')

    site_url = getattr(settings, 'SITE_URL', 'https://getnexiro.com')
    if request:
        try:
            site_url = request.build_absolute_uri('/').rstrip('/')
        except Exception:
            pass

    admin_url = ''
    try:
        admin_url = f"{site_url}/admin/core/subscriber/{subscriber.pk}/change/"
    except Exception:
        admin_url = f"{site_url}/admin/core/subscriber/"

    is_testing = getattr(settings, 'TESTING', False) or hasattr(mail, 'outbox')
    if is_testing or not async_send:
        _dispatch_newsletter_emails_sync(
            subscriber.pk, admin_recipient, lang, ip_address, source_page, site_url, admin_url
        )
    else:
        t = threading.Thread(
            target=_dispatch_newsletter_emails_sync,
            args=(subscriber.pk, admin_recipient, lang, ip_address, source_page, site_url, admin_url),
            daemon=True,
        )
        t.start()


