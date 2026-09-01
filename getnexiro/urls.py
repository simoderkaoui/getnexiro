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

# Language-prefixed URL patterns
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    prefix_default_language=True,
)
