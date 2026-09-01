"""
Core app views for getNexiro.

Each view renders a page of the agency website.
The contact view handles both GET (display form) and POST (process submission).
"""

from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.contrib import messages
from .forms import ContactForm


def home(request):
    """Landing page: hero, value proposition, featured services, project previews, CTA."""
    # Featured services data (icon class, title key, description key)
    featured_services = [
        {
            'icon': 'icon-web',
            'title': _('Web Development'),
            'description': _('Scalable web applications built with cutting-edge frameworks and architectures.'),
        },
        {
            'icon': 'icon-mobile',
            'title': _('Mobile Apps'),
            'description': _('Native and cross-platform mobile experiences that delight users.'),
        },
        {
            'icon': 'icon-design',
            'title': _('UI/UX Design'),
            'description': _('Research-driven design that balances aesthetics with usability.'),
        },
    ]

    # Featured projects preview
    featured_projects = [
        {
            'title': _('FinFlow Dashboard'),
            'category': _('FinTech'),
            'image': 'https://picsum.photos/seed/finflow/600/400',
        },
        {
            'title': _('MedConnect Platform'),
            'category': _('HealthTech'),
            'image': 'https://picsum.photos/seed/medconnect/600/400',
        },
        {
            'title': _('LogiTrack System'),
            'category': _('Logistics'),
            'image': 'https://picsum.photos/seed/logitrack/600/400',
        },
    ]

    context = {
        'featured_services': featured_services,
        'featured_projects': featured_projects,
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About page: agency story, mission, why Tangier, team, values."""
    team_members = [
        {
            'name': 'Youssef El Amrani',
            'role': _('CEO & Founder'),
            'image': 'https://picsum.photos/seed/youssef/300/300',
        },
        {
            'name': 'Amina Benali',
            'role': _('Lead Designer'),
            'image': 'https://picsum.photos/seed/amina/300/300',
        },
        {
            'name': 'Karim Tazi',
            'role': _('CTO'),
            'image': 'https://picsum.photos/seed/karim/300/300',
        },
        {
            'name': 'Sara Idrissi',
            'role': _('Project Manager'),
            'image': 'https://picsum.photos/seed/sara/300/300',
        },
    ]

    values = [
        {
            'title': _('Excellence'),
            'description': _('We pursue the highest standards in every line of code and pixel of design.'),
        },
        {
            'title': _('Innovation'),
            'description': _('We embrace emerging technologies to deliver future-proof solutions.'),
        },
        {
            'title': _('Transparency'),
            'description': _('Open communication and honest collaboration at every stage.'),
        },
        {
            'title': _('Partnership'),
            'description': _('We see ourselves as an extension of your team, not just a vendor.'),
        },
    ]

    context = {
        'team_members': team_members,
        'values': values,
    }
    return render(request, 'core/about.html', context)


def services(request):
    """Services page: full list of offered services with icons and descriptions."""
    services_list = [
        {
            'icon': 'icon-web',
            'title': _('Web Development'),
            'description': _('From responsive marketing sites to complex SaaS platforms, we architect and build robust web solutions using Django, React, and modern frameworks.'),
        },
        {
            'icon': 'icon-mobile',
            'title': _('Mobile Applications'),
            'description': _('Native iOS/Android and cross-platform apps built with Flutter and React Native, delivering seamless performance and beautiful interfaces.'),
        },
        {
            'icon': 'icon-design',
            'title': _('UI/UX Design'),
            'description': _('User research, wireframing, prototyping, and pixel-perfect design systems that elevate your brand and convert visitors into customers.'),
        },
        {
            'icon': 'icon-consulting',
            'title': _('Technical Consulting'),
            'description': _('Architecture reviews, technology audits, and strategic roadmapping to ensure your digital investments deliver maximum ROI.'),
        },
        {
            'icon': 'icon-api',
            'title': _('API & Integration'),
            'description': _('RESTful and GraphQL APIs, third-party integrations, and microservices architecture designed for scalability and reliability.'),
        },
        {
            'icon': 'icon-cloud',
            'title': _('Cloud & DevOps'),
            'description': _('Cloud infrastructure, CI/CD pipelines, containerization, and monitoring — we ensure your applications run flawlessly at any scale.'),
        },
    ]

    context = {
        'services_list': services_list,
    }
    return render(request, 'core/services.html', context)


def projects(request):
    """Projects page: portfolio grid with category filtering."""
    # Project categories for filtering
    categories = [
        {'slug': 'all', 'name': _('All')},
        {'slug': 'fintech', 'name': _('FinTech')},
        {'slug': 'healthtech', 'name': _('HealthTech')},
        {'slug': 'ecommerce', 'name': _('E-Commerce')},
        {'slug': 'logistics', 'name': _('Logistics')},
        {'slug': 'saas', 'name': _('SaaS')},
    ]

    projects_list = [
        {
            'title': _('FinFlow Dashboard'),
            'category': 'fintech',
            'category_label': _('FinTech'),
            'description': _('Real-time financial analytics dashboard for a leading investment firm.'),
            'image': 'https://picsum.photos/seed/proj1/600/400',
        },
        {
            'title': _('MedConnect Platform'),
            'category': 'healthtech',
            'category_label': _('HealthTech'),
            'description': _('Telemedicine platform connecting patients with specialists across Morocco.'),
            'image': 'https://picsum.photos/seed/proj2/600/400',
        },
        {
            'title': _('ShopLux E-Commerce'),
            'category': 'ecommerce',
            'category_label': _('E-Commerce'),
            'description': _('Premium e-commerce experience for a luxury fashion brand.'),
            'image': 'https://picsum.photos/seed/proj3/600/400',
        },
        {
            'title': _('LogiTrack System'),
            'category': 'logistics',
            'category_label': _('Logistics'),
            'description': _('End-to-end supply chain management system with real-time GPS tracking.'),
            'image': 'https://picsum.photos/seed/proj4/600/400',
        },
        {
            'title': _('CloudMetrics SaaS'),
            'category': 'saas',
            'category_label': _('SaaS'),
            'description': _('Multi-tenant analytics platform serving 500+ enterprise clients.'),
            'image': 'https://picsum.photos/seed/proj5/600/400',
        },
        {
            'title': _('PaySecure Gateway'),
            'category': 'fintech',
            'category_label': _('FinTech'),
            'description': _('PCI-compliant payment gateway processing millions of daily transactions.'),
            'image': 'https://picsum.photos/seed/proj6/600/400',
        },
    ]

    context = {
        'categories': categories,
        'projects_list': projects_list,
    }
    return render(request, 'core/projects.html', context)


def store(request):
    """Store page: coming soon placeholder."""
    return render(request, 'core/store.html')


def contact(request):
    """Contact page: form + agency address / map placeholder."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # In production, send email here. For now, show success message.
            messages.success(request, _('Thank you for your message! We will get back to you shortly.'))
            return redirect('core:contact')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'core/contact.html', context)
