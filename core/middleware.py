"""
getNexiro — Custom Middleware for Canonical Host, URL normalization, and SEO hygiene.
"""

import urllib.parse
from django.http import HttpResponsePermanentRedirect
from django.conf import settings


def normalize_uri(path):
    """
    Decodes percent-encoded characters and repairs latin-1 decoded UTF-8 mojibake
    commonly introduced by WSGI servers like Apache mod_passenger.
    """
    if not path:
        return path
    if '%' in path:
        try:
            path = urllib.parse.unquote(path, encoding='utf-8')
        except Exception:
            pass
    try:
        path = path.encode('iso-8859-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    return path


CANONICAL_SLUGS = {
    'en': {
        'about': 'about', 'a-propos': 'about', 'من-نحن': 'about',
        'services': 'services', 'خدمات': 'services',
        'projects': 'projects', 'projets': 'projects', 'مشاريع': 'projects',
        'blog': 'blog', 'مدونة': 'blog',
        'contact': 'contact', 'تواصل': 'contact',
    },
    'fr': {
        'about': 'a-propos', 'a-propos': 'a-propos', 'من-نحن': 'a-propos',
        'services': 'services', 'خدمات': 'services',
        'projects': 'projets', 'projets': 'projets', 'مشاريع': 'projets',
        'blog': 'blog', 'مدونة': 'blog',
        'contact': 'contact', 'تواصل': 'contact',
    },
    'ar': {
        'about': 'من-نحن', 'a-propos': 'من-نحن', 'من-نحن': 'من-نحن',
        'services': 'خدمات', 'خدمات': 'خدمات',
        'projects': 'مشاريع', 'projets': 'مشاريع', 'مشاريع': 'مشاريع',
        'blog': 'مدونة', 'مدونة': 'مدونة',
        'contact': 'تواصل', 'تواصل': 'تواصل',
    },
}

NON_PREFIX_MAP = {
    'من-نحن': '/ar/من-نحن/',
    'خدمات': '/ar/خدمات/',
    'مشاريع': '/ar/مشاريع/',
    'مدونة': '/ar/مدونة/',
    'تواصل': '/ar/تواصل/',
    'a-propos': '/fr/a-propos/',
    'projets': '/fr/projets/',
}


class CanonicalHostMiddleware:
    """
    Enforces canonical non-www host redirect (e.g. www.getnexiro.com -> getnexiro.com).
    Ensures a single 301 hop without duplicate redirects.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0].lower()
        if host == 'www.getnexiro.com':
            path = request.get_full_path()
            target = f"https://getnexiro.com{path}"
            return HttpResponsePermanentRedirect(target)
        return self.get_response(request)


class UrlNormalizationMiddleware:
    """
    1. Unquotes non-ASCII / Arabic percent-encoded paths (e.g. /ar/%D9%85%D9%86-%D9%86%D8%AD%D9%86/ -> /ar/من-نحن/)
       so Django's URL resolver matches translated route patterns cleanly.
    2. Handles 301 redirects for language slug aliases (e.g. /ar/about/ -> /ar/من-نحن/, /fr/about/ -> /fr/a-propos/)
       ensuring 0 broken links across languages and perfect SEO parity.
    3. Handles 301 redirects for unprefixed translated routes (e.g. /من-نحن/ -> /ar/من-نحن/).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Normalize path_info and path
        request.path_info = normalize_uri(request.path_info)
        request.path = normalize_uri(request.path)

        path = request.path_info

        # Skip static / media / admin / robots / sitemap
        if path.startswith(('/static/', '/media/', '/admin/', '/robots.txt', '/sitemap.xml', '/i18n/')):
            return self.get_response(request)

        # 2. Check for language slug redirect (e.g. /ar/about/ -> /ar/من-نحن/)
        parts = path.strip('/').split('/')
        if parts and parts[0] in CANONICAL_SLUGS and len(parts) >= 2:
            lang = parts[0]
            section = parts[1]
            canonical = CANONICAL_SLUGS[lang].get(section)
            if canonical and canonical != section:
                rest = '/' + '/'.join(parts[2:]) if len(parts) > 2 else ''
                trailing = '/' if path.endswith('/') else ''
                target = f"/{lang}/{canonical}{rest}{trailing}"
                qs = request.META.get('QUERY_STRING')
                if qs:
                    target += f"?{qs}"
                return HttpResponsePermanentRedirect(target)

        # 3. Check for unprefixed localized slug (e.g. /من-نحن/ -> /ar/من-نحن/)
        if parts and parts[0] in NON_PREFIX_MAP:
            target_base = NON_PREFIX_MAP[parts[0]].rstrip('/')
            rest = '/' + '/'.join(parts[1:]) if len(parts) > 1 else ''
            target = f"{target_base}{rest}/"
            qs = request.META.get('QUERY_STRING')
            if qs:
                target += f"?{qs}"
            return HttpResponsePermanentRedirect(target)

        return self.get_response(request)
