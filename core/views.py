"""
getNexiro — Core Views.

All content is fetched from the database (admin-editable).
Falls back to empty lists gracefully if no data exists yet.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.contrib import messages
from .forms import ContactForm
from .models import (
    SiteConfig, Service, ServiceSolution, ProjectCategory, Project,
    TeamMember, Testimonial, ClientLogo, Stat, ContactMessage,
    CompanyValue, ProcessStep, BlogCategory, BlogPost,
)
from .emails import send_contact_emails


def _get_common_context():
    """Returns context shared by all pages (site config, stats, etc.)."""
    return {
        'config': SiteConfig.load(),
    }


def home(request):
    """Landing page: hero, stats, value proposition, services preview, projects preview, testimonials, CTA."""
    ctx = _get_common_context()
    ctx.update({
        'featured_services': Service.objects.filter(is_featured=True)[:6],
        'featured_projects': Project.objects.filter(is_featured=True)[:6],
        'stats': Stat.objects.all()[:4],
        'testimonials': Testimonial.objects.filter(is_featured=True)[:3],
        'client_logos': ClientLogo.objects.all()[:8],
        'latest_posts': BlogPost.objects.filter(status='published')[:3],
    })
    return render(request, 'core/home.html', ctx)


def about(request):
    """About page: story, mission, Tangier advantage, team, values."""
    ctx = _get_common_context()
    ctx.update({
        'team_members': TeamMember.objects.all(),
        'company_values': CompanyValue.objects.all(),
    })
    return render(request, 'core/about.html', ctx)


def services(request):
    """Services page: full list of all services."""
    ctx = _get_common_context()
    ctx.update({
        'services_list': Service.objects.all(),
        'process_steps': ProcessStep.objects.all(),
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


def project_detail(request, slug):
    """Case study detail page with gallery carousel, tech stack, deep-dive story, and CTAs."""
    ctx = _get_common_context()
    project = get_object_or_404(
        Project.objects.select_related('category').prefetch_related('gallery_images'),
        slug=slug
    )

    gallery_images = list(project.gallery_images.all())

    # Related projects
    related_projects = Project.objects.filter(category=project.category).exclude(pk=project.pk)[:3]
    if not related_projects.exists():
        related_projects = Project.objects.exclude(pk=project.pk)[:3]

    ctx.update({
        'project': project,
        'gallery_images': gallery_images,
        'related_projects': related_projects,
    })
    return render(request, 'core/project_detail.html', ctx)


def service_detail(request, slug):
    """Service detail page with solutions grid, methodology, deliverables, tech stack, and CTAs."""
    ctx = _get_common_context()
    service = get_object_or_404(
        Service.objects.prefetch_related('solutions'),
        slug=slug
    )

    # Related services (same order, exclude current)
    related_services = Service.objects.exclude(pk=service.pk)[:3]

    ctx.update({
        'service': service,
        'related_services': related_services,
    })
    return render(request, 'core/service_detail.html', ctx)


def blog(request):
    """Blog listing page with SEO-optimized structure."""
    ctx = _get_common_context()
    category_slug = request.GET.get('category')
    posts = BlogPost.objects.filter(status='published').select_related('category')

    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    ctx.update({
        'posts': posts,
        'categories': BlogCategory.objects.all(),
        'active_category': category_slug,
    })
    return render(request, 'core/blog.html', ctx)


def blog_detail(request, slug):
    """Individual blog post with full SEO meta, structured data, and related posts."""
    ctx = _get_common_context()
    post = get_object_or_404(
        BlogPost.objects.select_related('category'),
        slug=slug, status='published'
    )

    related_posts = BlogPost.objects.filter(
        status='published', category=post.category
    ).exclude(pk=post.pk)[:3]
    if not related_posts.exists():
        related_posts = BlogPost.objects.filter(status='published').exclude(pk=post.pk)[:3]

    ctx.update({
        'post': post,
        'related_posts': related_posts,
    })
    return render(request, 'core/blog_detail.html', ctx)


def contact(request):
    """Contact page: form + info. Saves submissions to DB."""
    ctx = _get_common_context()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
            )
            # Dispatch both admin notification and sender confirmation emails
            send_contact_emails(contact_msg, request=request)

            messages.success(request, _('Thank you for your message! We will get back to you shortly.'))
            return redirect('core:contact')
    else:
        form = ContactForm()

    ctx['form'] = form
    return render(request, 'core/contact.html', ctx)
