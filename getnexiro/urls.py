"""
getNexiro — Root URL Configuration

Includes:
- i18n URL patterns with language prefix (en/, fr/, ar/)
- Language switcher endpoint (i18n/setlang/)
- Core app URLs
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

# Non-prefixed URLs (language switcher endpoint)
urlpatterns = [
    # Django's built-in set_language view for the language switcher
    path('i18n/', include('django.conf.urls.i18n')),
]

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

# Language-prefixed URL patterns
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
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
