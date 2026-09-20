"""
Core app URL configuration.

Maps all main pages: Home, About, Services, Projects, Blog, Contact.
URL path segments are translated for SEO (e.g. /fr/services/ vs /ar/خدمات/).
"""

from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path(_('about/'), views.about, name='about'),
    path(_('services/'), views.services, name='services'),
    path(_('services/') + '<slug:slug>/', views.service_detail, name='service_detail'),
    path(_('projects/'), views.projects, name='projects'),
    path(_('projects/') + '<slug:slug>/', views.project_detail, name='project_detail'),
    path(_('blog/'), views.blog, name='blog'),
    path(_('blog/') + '<slug:slug>/', views.blog_detail, name='blog_detail'),
    path(_('contact/'), views.contact, name='contact'),
]
