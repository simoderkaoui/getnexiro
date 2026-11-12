"""
getNexiro — Custom Middleware for Canonical Host and SEO hygiene.
"""

from django.http import HttpResponsePermanentRedirect
from django.conf import settings


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
