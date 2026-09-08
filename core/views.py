"""
getNexiro — Core Views.

All content is fetched from the database (admin-editable).
Falls back to empty lists gracefully if no data exists yet.
"""

from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.contrib import messages
from .forms import ContactForm
from .models import (
    SiteConfig, Service, ProjectCategory, Project,
    TeamMember, Testimonial, ClientLogo, Stat, ContactMessage,
)


def _get_common_context():
    """Returns context shared by all pages (site config, stats, etc.)."""
    return {
        'config': SiteConfig.load(),
    }


def home(request):
    """Landing page: hero, stats, value proposition, services preview, projects preview, testimonials, CTA."""
    ctx = _get_common_context()
    ctx.update({
        'featured_services': Service.objects.filter(is_featured=True)[:3],
        'featured_projects': Project.objects.filter(is_featured=True)[:3],
        'stats': Stat.objects.all()[:4],
        'testimonials': Testimonial.objects.filter(is_featured=True)[:3],
        'client_logos': ClientLogo.objects.all()[:8],
    })
    return render(request, 'core/home.html', ctx)


def about(request):
    """About page: story, mission, Tangier advantage, team, values."""
    ctx = _get_common_context()
    ctx.update({
        'team_members': TeamMember.objects.all(),
    })
    return render(request, 'core/about.html', ctx)


def services(request):
    """Services page: full list of all services."""
    ctx = _get_common_context()
    ctx.update({
        'services_list': Service.objects.all(),
    })
    return render(request, 'core/services.html', ctx)


def projects(request):
    """Projects page: portfolio grid with category filtering."""
    ctx = _get_common_context()
    ctx.update({
        'categories': ProjectCategory.objects.all(),
        'projects_list': Project.objects.select_related('category').all(),
    })
    return render(request, 'core/projects.html', ctx)


def store(request):
    """Store page: coming soon placeholder."""
    ctx = _get_common_context()
    return render(request, 'core/store.html', ctx)


def contact(request):
    """Contact page: form + info. Saves submissions to DB."""
    ctx = _get_common_context()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
            )
            messages.success(request, _('Thank you for your message! We will get back to you shortly.'))
            return redirect('core:contact')
    else:
        form = ContactForm()

    ctx['form'] = form
    return render(request, 'core/contact.html', ctx)
