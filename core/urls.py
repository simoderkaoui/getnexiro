"""
Core app URL configuration.

Maps all main pages: Home, About, Services, Projects, Store, Contact.
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('store/', views.store, name='store'),
    path('contact/', views.contact, name='contact'),
]
