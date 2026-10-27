"""
Context processors for getNexiro.
Provides global template variables: SITE_URL, ANALYTICS_PROVIDER, ANALYTICS_ID, LANGUAGE_BIDI.
"""

from django.conf import settings


def site_settings(request):
    """Expose key settings to all templates."""
    return {
        'SITE_URL': getattr(settings, 'SITE_URL', 'https://getnexiro.com'),
        'ANALYTICS_PROVIDER': getattr(settings, 'ANALYTICS_PROVIDER', ''),
        'ANALYTICS_ID': getattr(settings, 'ANALYTICS_ID', ''),
    }
