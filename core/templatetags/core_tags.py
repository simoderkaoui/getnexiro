from django import template
from django.urls import translate_url as django_translate_url

register = template.Library()


@register.filter(name='translate_url')
def translate_url(url, lang_code):
    """
    Given a URL path and a target language code, translate the URL
    to the target language route (e.g. /fr/a-propos/ -> /ar/من-نحن/).
    Falls back gracefully if URL cannot be reversed.
    """
    if not url:
        return f'/{lang_code}/'
    try:
        translated = django_translate_url(url, lang_code)
        return translated if translated else url
    except Exception:
        return url
