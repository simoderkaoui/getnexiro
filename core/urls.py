"""
Core app URL configuration.

Maps all main pages: Home, About, Services, Projects, Blog, Contact, Legal.
URL path segments are translated for SEO (e.g. /fr/services/ vs /ar/خدمات/).
"""

from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path(_('about/'), views.about, name='about'),
    path(_('services/'), include([
        path('', views.services, name='services'),
        path('<slug:slug>/', views.service_detail, name='service_detail'),
    ])),
    path(_('projects/'), include([
        path('', views.projects, name='projects'),
        path('<slug:slug>/', views.project_detail, name='project_detail'),
    ])),
    path(_('blog/'), include([
        path('', views.blog, name='blog'),
        path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    ])),
    path(_('contact/'), views.contact, name='contact'),

    # Legal pages
    path(_('privacy-policy/'), views.legal_page, {'slug': 'privacy-policy'}, name='privacy_policy'),
    path(_('terms-of-service/'), views.legal_page, {'slug': 'terms-of-service'}, name='terms_of_service'),
]
