"""
Core app URL configuration.

Maps all main pages: Home, About, Services, Projects, Blog, Contact, Legal, Quote, Booking, Packages.
URL path segments are translated for SEO (e.g. /fr/services/ vs /ar/خدمات/).
"""

from django.urls import path, include
from . import views

app_name = 'core'

# Canonical ASCII URL patterns across all languages (en, fr, ar)
# Prevents Apache / Passenger WSGI non-ASCII path mangling
# All legacy localized aliases (e.g. /ar/من-نحن/, /ar/خدمات/, /fr/a-propos/)
# 301 permanently redirect to these canonical routes via UrlNormalizationMiddleware.
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', include([
        path('', views.services, name='services'),
        path('<slug:slug>/', views.service_detail, name='service_detail'),
        path('<slug:service_slug>/<slug:city_slug>/', views.city_service_page, name='city_service_page'),
    ])),
    path('projects/', include([
        path('', views.projects, name='projects'),
        path('<slug:slug>/', views.project_detail, name='project_detail'),
    ])),
    path('blog/', include([
        path('', views.blog, name='blog'),
        path('feed/', views.blog_rss_feed, name='blog_rss_feed'),
        path('author/<slug:slug>/', views.author_detail, name='author_detail'),
        path('category/<slug:slug>/', views.blog_category_archive, name='blog_category_archive'),
        path('tag/<path:tag>/', views.blog_tag_archive, name='blog_tag_archive'),
        path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    ])),
    path('contact/', views.contact, name='contact'),

    # Legal pages
    path('privacy-policy/', views.legal_page, {'slug': 'privacy-policy'}, name='privacy_policy'),
    path('terms-of-service/', views.legal_page, {'slug': 'terms-of-service'}, name='terms_of_service'),

    # Lead Generation & Booking
    path('quote/', views.quote_wizard, name='quote_wizard'),
    path('quote/success/', views.quote_success, name='quote_success'),
    path('packages/', views.packages, name='packages'),
    path('booking/', views.booking, name='booking'),
    path('checklist/', views.lead_magnet, name='lead_magnet'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('confirm/<str:token>/', views.confirm_subscription, name='confirm_subscription'),
]
