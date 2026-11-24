import sys
import socket
from django.core.management.base import BaseCommand
from django.core.mail import get_connection, EmailMultiAlternatives
from django.conf import settings
from email.utils import parseaddr, formataddr


class Command(BaseCommand):
    help = 'Diagnose and test the live SMTP email configuration by sending a test message.'

    def add_arguments(self, parser):
        parser.add_argument(
            'recipient',
            nargs='?',
            default='contact@getnexiro.com',
            help='Recipient email address to test delivery (defaults to contact@getnexiro.com).'
        )

    def handle(self, *args, **options):
        recipient = options['recipient']
        self.stdout.write(self.style.MIGRATE_HEADING("\n=== getNexiro SMTP Configuration Diagnostic ==="))

        backend = getattr(settings, 'EMAIL_BACKEND', '')
        host = getattr(settings, 'EMAIL_HOST', '')
        port = getattr(settings, 'EMAIL_PORT', '')
        use_tls = getattr(settings, 'EMAIL_USE_TLS', False)
        use_ssl = getattr(settings, 'EMAIL_USE_SSL', False)
        user = getattr(settings, 'EMAIL_HOST_USER', '')
        pwd = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', '')
        timeout = getattr(settings, 'EMAIL_TIMEOUT', 10)

        self.stdout.write(f"EMAIL_BACKEND:       {backend}")
        self.stdout.write(f"EMAIL_HOST:          {host}")
        self.stdout.write(f"EMAIL_PORT:          {port}")
        self.stdout.write(f"EMAIL_USE_TLS:       {use_tls}")
        self.stdout.write(f"EMAIL_USE_SSL:       {use_ssl}")
        self.stdout.write(f"EMAIL_HOST_USER:     {user or '(NOT SET - EMPTY!)'}")
        self.stdout.write(f"EMAIL_HOST_PASSWORD: {'*' * len(pwd) if pwd else '(NOT SET - EMPTY!)'}")
        self.stdout.write(f"DEFAULT_FROM_EMAIL:  {from_email}")
        self.stdout.write(f"EMAIL_TIMEOUT:       {timeout}s")

        if 'console.EmailBackend' in backend:
            self.stdout.write(self.style.ERROR(
                "\n[WARNING] Django is currently using the CONSOLE email backend!\n"
                "Emails are being printed to server logs/stdout instead of being sent to real inboxes.\n"
                "Reason: EMAIL_HOST_USER is missing from your .env file or environment variables.\n"
                "To fix: Set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in your server .env file."
            ))
            return

        if not user or not pwd:
            self.stdout.write(self.style.WARNING(
                "\n[WARNING] EMAIL_HOST_USER or EMAIL_HOST_PASSWORD is empty. SMTP authentication may fail."
            ))

        # Test raw socket reachability first
        self.stdout.write(f"\n1. Testing network reachability to {host}:{port}...")
        try:
            s = socket.create_connection((host, int(port)), timeout=8)
            s.close()
            self.stdout.write(self.style.SUCCESS(f"   [OK] Successfully connected to {host}:{port} via TCP."))
        except Exception as net_err:
            self.stdout.write(self.style.ERROR(
                f"   [FAIL] Network connection to {host}:{port} failed: {net_err}\n"
                f"   Notice: Your hosting provider (e.g. cPanel) may be blocking outbound port {port}.\n"
                f"   If using cPanel webmail, try EMAIL_HOST=localhost with port 465 (SSL) or 25."
            ))
            return

        # Test Django SMTP connection
        self.stdout.write(f"\n2. Authenticating with SMTP server ({host})...")
        try:
            connection = get_connection(
                backend=backend,
                host=host,
                port=port,
                username=user,
                password=pwd,
                use_tls=use_tls,
                use_ssl=use_ssl,
                timeout=timeout,
            )
            connection.open()
            self.stdout.write(self.style.SUCCESS("   [OK] SMTP handshake and authentication successful!"))
        except Exception as auth_err:
            err_str = str(auth_err)
            if 'Hostname mismatch' in err_str or 'CERTIFICATE_VERIFY_FAILED' in err_str:
                self.stdout.write(self.style.ERROR(
                    f"   [FAIL] SSL Certificate verification failed: {auth_err}\n\n"
                    f"   SOLUTION FOR CPANEL:\n"
                    f"   Change EMAIL_HOST in your .env file to:\n"
                    f"     EMAIL_HOST=getnexiro.com\n"
                    f"   (Do NOT use mail.getnexiro.com because the SSL certificate is issued for getnexiro.com!)"
                ))
            else:
                self.stdout.write(self.style.ERROR(
                    f"   [FAIL] SMTP authentication failed: {auth_err}\n\n"
                    f"   Common solutions:\n"
                    f"   - If using Gmail: Standard passwords do NOT work. You must enable 2FA\n"
                    f"     and generate a 16-character App Password at https://myaccount.google.com/apppasswords\n"
                    f"   - If using cPanel email: Use EMAIL_HOST=getnexiro.com (or localhost),\n"
                    f"     EMAIL_PORT=465 with EMAIL_USE_SSL=True and your cPanel mailbox password."
                ))
            return

        # Attempt to deliver test email
        self.stdout.write(f"\n3. Sending test delivery message to {recipient}...")
        try:
            name, addr = parseaddr(from_email)
            if not addr:
                addr = user or 'contact@getnexiro.com'
            safe_from = formataddr((name or 'getNexiro Test', addr))

            subject = "[getNexiro SMTP Diagnostic] Live Email Test"
            body = (
                f"Hello,\n\n"
                f"This is a verified test email sent directly from the getNexiro Django server.\n\n"
                f"Configuration:\n"
                f"- Host: {host}:{port}\n"
                f"- User: {user}\n"
                f"- From: {safe_from}\n"
                f"- To: {recipient}\n\n"
                f"If you received this message, your outbound SMTP email system is 100% operational!\n\n"
                f"-- \ngetNexiro Engineering Studio"
            )

            msg = EmailMultiAlternatives(
                subject=subject,
                body=body,
                from_email=safe_from,
                to=[recipient],
                connection=connection,
            )
            sent_count = msg.send(fail_silently=False)
            connection.close()

            if sent_count > 0:
                self.stdout.write(self.style.SUCCESS(
                    f"\n[SUCCESS] Test email successfully delivered to {recipient}!\n"
                    f"Please check your inbox (and spam/junk folder just in case)."
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"\n[WARNING] Message was processed but sent count is 0."
                ))

        except Exception as send_err:
            self.stdout.write(self.style.ERROR(
                f"\n[FAIL] Failed to send email: {send_err}"
            ))
