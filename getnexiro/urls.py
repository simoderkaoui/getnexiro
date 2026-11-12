"""
getNexiro — Root URL Configuration

Includes:
- i18n URL patterns with language prefix (en/, fr/, ar/)
- Language switcher endpoint (i18n/setlang/)
- Core app URLs
- Custom error handlers (404, 500)
"""

from django.contrib import admin
from core.admin import nexiro_admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from django.views.generic import RedirectView

# Non-prefixed URLs (language switcher endpoint, SEO, icons)
from core.seo import robots_txt, sitemap_xml
urlpatterns = [
    # Permanent 301 redirect from root to default language (no 302 or Accept-Language sniffing)
    path('', RedirectView.as_view(url='/en/', permanent=True)),
    # Django's built-in set_language view for the language switcher
    path('i18n/', include('django.conf.urls.i18n')),
    # SEO: sitemap and robots
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap_xml'),
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
    path('site.webmanifest', RedirectView.as_view(url='/static/site.webmanifest', permanent=True)),
]

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

# Language-prefixed URL patterns
urlpatterns += i18n_patterns(
    path('admin/', nexiro_admin.urls),
    path('', include('core.urls')),
    prefix_default_language=True,
)

# Static & Media URL patterns (guaranteed serving)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Custom error handlers
handler404 = 'core.views.handler404_view'
handler500 = 'core.views.handler500_view'
