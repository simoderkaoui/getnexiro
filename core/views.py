"""
getNexiro — Core Views.

All content is fetched from the database (admin-editable).
Falls back to empty lists gracefully if no data exists yet.
"""

from decimal import Decimal
import json
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _, get_language
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import (
    ContactForm, QuoteStep1Form, QuoteStep2Form, QuoteStep3Form, QuoteStep4Form,
    BookingForm, SubscriberForm,
)
from .models import get_localized
from .models import (
    SiteConfig, Service, ServiceSolution, ProjectCategory, Project,
    TeamMember, Testimonial, ClientLogo, Stat, ContactMessage,
    CompanyValue, ProcessStep, BlogCategory, BlogPost,
    LegalPage, FAQ,
    Package, PricingRule, QuoteRequest,
    WeeklyAvailability, Booking, Subscriber,
    CityServicePage,
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
        'faqs': FAQ.objects.filter(is_active=True, section='general')[:6],
    })
    ctx['page_seo_title'] = get_localized(ctx['config'], 'home_seo_title')
    return render(request, 'core/home.html', ctx)


def about(request):
    """About page: story, mission, Tangier advantage, team, values."""
    ctx = _get_common_context()
    ctx.update({
        'team_members': TeamMember.objects.all(),
        'company_values': CompanyValue.objects.all(),
    })
    ctx['page_seo_title'] = get_localized(ctx['config'], 'about_seo_title')
    return render(request, 'core/about.html', ctx)


def services(request):
    """Services page: full list of all services."""
    ctx = _get_common_context()
    ctx.update({
        'services_list': Service.objects.all(),
        'process_steps': ProcessStep.objects.all(),
        'faqs': FAQ.objects.filter(is_active=True, section='services')[:6],
    })
    ctx['page_seo_title'] = get_localized(ctx['config'], 'services_seo_title')
    return render(request, 'core/services.html', ctx)


def projects(request):
    """Projects page: portfolio grid with category filtering."""
    ctx = _get_common_context()
    ctx.update({
        'categories': ProjectCategory.objects.all(),
        'projects_list': Project.objects.select_related('category').all(),
    })
    ctx['page_seo_title'] = get_localized(ctx['config'], 'projects_seo_title')
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
        'breadcrumbs': [
            {'name': _('Home'), 'url': reverse('core:home')},
            {'name': _('Projects'), 'url': reverse('core:projects')},
            {'name': project.title, 'url': request.path},
        ],
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
        'breadcrumbs': [
            {'name': _('Home'), 'url': reverse('core:home')},
            {'name': _('Services'), 'url': reverse('core:services')},
            {'name': service.title, 'url': request.path},
        ],
    })
    return render(request, 'core/service_detail.html', ctx)


def blog(request):
    """Blog listing page with SEO-optimized structure and search capability."""
    ctx = _get_common_context()
    category_slug = request.GET.get('category')
    search_query = (request.GET.get('search') or request.GET.get('q') or '').strip()
    posts = BlogPost.objects.filter(status='published').select_related('category')

    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    if search_query:
        from django.db.models import Q
        posts = posts.filter(
            Q(title_en__icontains=search_query) |
            Q(title_fr__icontains=search_query) |
            Q(title_ar__icontains=search_query) |
            Q(excerpt_en__icontains=search_query) |
            Q(excerpt_fr__icontains=search_query) |
            Q(excerpt_ar__icontains=search_query) |
            Q(body_en__icontains=search_query) |
            Q(body_fr__icontains=search_query) |
            Q(body_ar__icontains=search_query)
        )

    ctx.update({
        'posts': posts,
        'categories': BlogCategory.objects.all(),
        'active_category': category_slug,
        'search_query': search_query,
    })
    ctx['page_seo_title'] = get_localized(ctx['config'], 'blog_seo_title')
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
        'breadcrumbs': [
            {'name': _('Home'), 'url': reverse('core:home')},
            {'name': _('Blog'), 'url': reverse('core:blog')},
            {'name': post.title, 'url': request.path},
        ],
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
    ctx['page_seo_title'] = get_localized(ctx['config'], 'contact_seo_title')
    return render(request, 'core/contact.html', ctx)


# ── Legal Pages ──────────────────────────────────────────────────

def legal_page(request, slug):
    """Render a legal page (Privacy Policy, Terms, etc.) from the database."""
    page = get_object_or_404(LegalPage, slug=slug)
    ctx = _get_common_context()
    ctx['page'] = page
    return render(request, 'core/legal_page.html', ctx)


# ══════════════════════════════════════════════════════════════════
# PHASE 2: Lead Generation Views
# ══════════════════════════════════════════════════════════════════


def _compute_quote_estimate(project_type, features_str, num_pages, num_languages, timeline):
    """Calculate indicative price range from admin-editable PricingRules."""
    rules = PricingRule.objects.filter(is_active=True)
    base = Decimal('0')
    multiplier = Decimal('1.0')

    # Base price from project type
    type_rule = rules.filter(category='project_type', key=project_type).first()
    if type_rule:
        base += type_rule.value

    # Feature add-ons
    if features_str:
        feature_keys = [f.strip() for f in features_str.split(',') if f.strip()]
        for rule in rules.filter(category='feature', key__in=feature_keys):
            base += rule.value

    # Pages/screens
    if num_pages:
        pages_rule = rules.filter(category='pages', key=num_pages).first()
        if pages_rule:
            base += pages_rule.value

    # Additional languages (beyond 1)
    if num_languages and num_languages > 1:
        lang_rule = rules.filter(category='language').first()
        if lang_rule:
            base += lang_rule.value * (num_languages - 1)

    # Timeline multiplier
    if timeline:
        timeline_rule = rules.filter(category='timeline', key=timeline).first()
        if timeline_rule:
            multiplier = timeline_rule.value

    if base == 0:
        return None, None

    estimated = base * multiplier
    # Return a range: -15% to +25%
    est_min = int(estimated * Decimal('0.85'))
    est_max = int(estimated * Decimal('1.25'))
    return est_min, est_max


def quote_wizard(request):
    """Multi-step quote estimator wizard."""
    ctx = _get_common_context()

    # Get pricing rules for feature checkboxes
    feature_rules = PricingRule.objects.filter(category='feature', is_active=True).order_by('order')

    if request.method == 'POST':
        # Validate all steps at once on final submit
        form1 = QuoteStep1Form(request.POST)
        form2 = QuoteStep2Form(request.POST)
        form3 = QuoteStep3Form(request.POST)
        form4 = QuoteStep4Form(request.POST)

        all_valid = all([form1.is_valid(), form2.is_valid(), form3.is_valid(), form4.is_valid()])

        # Honeypot check
        if form4.is_valid() and form4.cleaned_data.get('website_url'):
            # Bot detected — silently accept
            messages.success(request, _('Thank you! Your quote request has been submitted.'))
            return redirect('core:quote_wizard')

        if all_valid:
            # Compute estimate
            est_min, est_max = _compute_quote_estimate(
                form1.cleaned_data['project_type'],
                form2.cleaned_data.get('features', ''),
                form2.cleaned_data.get('num_pages', ''),
                form2.cleaned_data.get('num_languages', 1),
                form3.cleaned_data.get('timeline', ''),
            )

            quote = QuoteRequest.objects.create(
                project_type=form1.cleaned_data['project_type'],
                project_description=form1.cleaned_data.get('project_description', ''),
                features=form2.cleaned_data.get('features', ''),
                num_pages=form2.cleaned_data.get('num_pages', ''),
                num_languages=form2.cleaned_data.get('num_languages', 1),
                timeline=form3.cleaned_data.get('timeline', ''),
                budget_range=form3.cleaned_data.get('budget_range', ''),
                name=form4.cleaned_data['name'],
                email=form4.cleaned_data['email'],
                phone=form4.cleaned_data.get('phone', ''),
                company=form4.cleaned_data.get('company', ''),
                estimated_min=est_min,
                estimated_max=est_max,
                source_page=request.META.get('HTTP_REFERER', ''),
            )

            # Send notification emails (reuse pattern from contact)
            try:
                from django.core.mail import EmailMultiAlternatives
                from django.conf import settings

                # Admin notification
                admin_subject = f'[getNexiro] New Quote Request from {quote.name}'
                admin_body = (
                    f"New quote request received:\n\n"
                    f"Name: {quote.name}\n"
                    f"Email: {quote.email}\n"
                    f"Phone: {quote.phone}\n"
                    f"Company: {quote.company}\n"
                    f"Project Type: {quote.get_project_type_display()}\n"
                    f"Description: {quote.project_description}\n"
                    f"Features: {quote.features}\n"
                    f"Pages: {quote.num_pages}\n"
                    f"Languages: {quote.num_languages}\n"
                    f"Timeline: {quote.timeline}\n"
                    f"Budget: {quote.budget_range}\n"
                    f"Estimate: {quote.estimated_min} — {quote.estimated_max} MAD\n"
                )
                admin_email = EmailMultiAlternatives(
                    subject=admin_subject,
                    body=admin_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.DEFAULT_FROM_EMAIL],
                )
                admin_email.send(fail_silently=True)

                # Visitor confirmation (Multilingual EN/FR/AR)
                user_lang = getattr(request, 'LANGUAGE_CODE', None) or 'en'
                if user_lang.startswith('fr'):
                    visitor_subject = "Votre demande de devis getNexiro a bien été reçue !"
                    visitor_body = (
                        f"Bonjour {quote.name},\n\n"
                        f"Merci pour votre demande de devis ! Nous avons bien reçu les détails de votre projet et "
                        f"nous vous recontacterons sous 24 heures avec une proposition détaillée.\n\n"
                    )
                    if est_min and est_max:
                        visitor_body += f"Estimation indicative : {est_min:,} — {est_max:,} MAD\n\n"
                    visitor_body += (
                        f"En attendant, vous pouvez planifier un appel de découverte ou nous joindre sur WhatsApp.\n\n"
                        f"Cordialement,\nL'équipe getNexiro\n"
                    )
                elif user_lang.startswith('ar'):
                    visitor_subject = "تم استلام طلب عرض السعر — getNexiro"
                    visitor_body = (
                        f"مرحباً {quote.name}،\n\n"
                        f"شكراً لاهتمامك بخدماتنا! لقد استلمنا تفاصيل مشروعك وسنتواصل معك خلال 24 ساعة بمقترح تقني ومالي مفصل.\n\n"
                    )
                    if est_min and est_max:
                        visitor_body += f"التقدير الأولي للمشروع: {est_min:,} — {est_max:,} درهم مغربي\n\n"
                    visitor_body += (
                        f"يمكنك أيضاً حجز مكالمة استكشافية مباشرة أو مراسلتنا عبر واتساب.\n\n"
                        f"مع خالص التحية،\nفريق عمل getNexiro\n"
                    )
                else:
                    visitor_subject = "Your getNexiro Quote Request — Received!"
                    visitor_body = (
                        f"Hi {quote.name},\n\n"
                        f"Thank you for your quote request! We've received your project details and "
                        f"will get back to you within 24 hours with a detailed proposal.\n\n"
                    )
                    if est_min and est_max:
                        visitor_body += f"Indicative estimate: {est_min:,} — {est_max:,} MAD\n\n"
                    visitor_body += (
                        f"In the meantime, feel free to book a discovery call or reach us on WhatsApp.\n\n"
                        f"Best regards,\nThe getNexiro Team\n"
                    )

                visitor_email = EmailMultiAlternatives(
                    subject=visitor_subject,
                    body=visitor_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[quote.email],
                )
                visitor_email.extra_headers['Auto-Submitted'] = 'auto-replied'
                visitor_email.extra_headers['X-Auto-Response-Suppress'] = 'All'
                visitor_email.extra_headers['Precedence'] = 'auto_reply'
                visitor_email.send(fail_silently=True)
            except Exception:
                pass  # Form saved to DB even if email fails

            # Redirect to success page with estimate
            request.session['quote_submitted'] = True
            request.session['quote_id'] = quote.pk
            return redirect('core:quote_success')

        ctx.update({
            'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4,
            'feature_rules': feature_rules,
        })
    else:
        # Pre-fill from package CTA
        initial1 = {}
        prefill = request.GET.get('type', '')
        if prefill:
            initial1['project_type'] = prefill

        ctx.update({
            'form1': QuoteStep1Form(initial=initial1),
            'form2': QuoteStep2Form(),
            'form3': QuoteStep3Form(),
            'form4': QuoteStep4Form(),
            'feature_rules': feature_rules,
        })

    return render(request, 'core/quote_wizard.html', ctx)


def quote_success(request):
    """Quote submission success page with estimate."""
    if not request.session.get('quote_submitted'):
        return redirect('core:quote_wizard')

    ctx = _get_common_context()
    quote_id = request.session.pop('quote_id', None)
    request.session.pop('quote_submitted', None)

    if quote_id:
        try:
            quote = QuoteRequest.objects.get(pk=quote_id)
            ctx['quote'] = quote
        except QuoteRequest.DoesNotExist:
            pass

    return render(request, 'core/quote_success.html', ctx)


def packages(request):
    """Pricing packages page."""
    ctx = _get_common_context()
    ctx.update({
        'packages': Package.objects.filter(is_active=True).prefetch_related('features'),
        'faqs': FAQ.objects.filter(is_active=True, section='pricing')[:6],
    })
    ctx['page_seo_title'] = get_localized(ctx['config'], 'packages_seo_title')
    return render(request, 'core/packages.html', ctx)


def booking(request):
    """Discovery call booking page."""
    ctx = _get_common_context()

    # Get available weekly slots
    available_slots = WeeklyAvailability.objects.filter(is_active=True)

    if request.method == 'POST':
        form = BookingForm(request.POST)

        # Honeypot check
        if form.is_valid() and form.cleaned_data.get('website_url'):
            messages.success(request, _('Your booking has been confirmed!'))
            return redirect('core:booking')

        if form.is_valid():
            book_date = form.cleaned_data['date']
            book_time = form.cleaned_data['time_slot']

            # Check if slot is available
            if Booking.objects.filter(date=book_date, time_slot=book_time).exclude(status='cancelled').exists():
                form.add_error('time_slot', _('This time slot is already booked. Please choose another.'))
            else:
                bk = Booking.objects.create(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data.get('phone', ''),
                    company=form.cleaned_data.get('company', ''),
                    date=book_date,
                    time_slot=book_time,
                    timezone_name=form.cleaned_data.get('timezone_name', 'Africa/Casablanca'),
                    message=form.cleaned_data.get('message', ''),
                    source_page=request.META.get('HTTP_REFERER', ''),
                )

                # Send emails
                try:
                    from django.core.mail import EmailMultiAlternatives
                    from django.conf import settings

                    admin_email = EmailMultiAlternatives(
                        subject=f'[getNexiro] New Booking from {bk.name} — {bk.date} at {bk.time_slot}',
                        body=(
                            f"New discovery call booked:\n\n"
                            f"Name: {bk.name}\nEmail: {bk.email}\nPhone: {bk.phone}\n"
                            f"Company: {bk.company}\nDate: {bk.date}\nTime: {bk.time_slot}\n"
                            f"Message: {bk.message}\n"
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[settings.DEFAULT_FROM_EMAIL],
                    )
                    admin_email.send(fail_silently=True)

                    user_lang = getattr(request, 'LANGUAGE_CODE', None) or 'en'
                    if user_lang.startswith('fr'):
                        visitor_subject = "Votre appel de découverte avec getNexiro est confirmé !"
                        visitor_body = (
                            f"Bonjour {bk.name},\n\n"
                            f"Votre appel de découverte est bien confirmé !\n\n"
                            f"Date : {bk.date.strftime('%d/%m/%Y')}\n"
                            f"Heure : {bk.time_slot.strftime('%H:%M')} (GMT+1 / Heure du Maroc)\n\n"
                            f"Nous vous contacterons à l'adresse e-mail ou au numéro de téléphone indiqué.\n\n"
                            f"Ajouter à Google Agenda :\n{bk.google_calendar_url}\n\n"
                            f"Cordialement,\nL'équipe getNexiro\n"
                        )
                    elif user_lang.startswith('ar'):
                        visitor_subject = "تم تأكيد مكالمتك الاستكشافية مع getNexiro!"
                        visitor_body = (
                            f"مرحباً {bk.name}،\n\n"
                            f"تم تأكيد موعد مكالمتك الاستكشافية بنجاح!\n\n"
                            f"التاريخ: {bk.date.strftime('%Y-%m-%d')}\n"
                            f"الوقت: {bk.time_slot.strftime('%H:%M')} (بتوقيت المغرب GMT+1)\n\n"
                            f"سيتواصل معك فريقنا الهندسي عبر الهاتف أو البريد الإلكتروني المحدد.\n\n"
                            f"إضافة إلى تقويم Google:\n{bk.google_calendar_url}\n\n"
                            f"مع أطيب التحيات،\nفريق getNexiro\n"
                        )
                    else:
                        visitor_subject = "Your getNexiro Discovery Call — Confirmed!"
                        visitor_body = (
                            f"Hi {bk.name},\n\n"
                            f"Your discovery call is confirmed!\n\n"
                            f"Date: {bk.date.strftime('%A, %B %d, %Y')}\n"
                            f"Time: {bk.time_slot.strftime('%H:%M')} (GMT+1 / Morocco time)\n\n"
                            f"We'll contact you at the provided email or phone number.\n\n"
                            f"Add to Google Calendar:\n{bk.google_calendar_url}\n\n"
                            f"Best regards,\nThe getNexiro Team\n"
                        )

                    visitor_email = EmailMultiAlternatives(
                        subject=visitor_subject,
                        body=visitor_body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[bk.email],
                    )
                    visitor_email.extra_headers['Auto-Submitted'] = 'auto-replied'
                    visitor_email.extra_headers['X-Auto-Response-Suppress'] = 'All'
                    visitor_email.extra_headers['Precedence'] = 'auto_reply'
                    visitor_email.send(fail_silently=True)
                except Exception:
                    pass

                messages.success(request, _('Your discovery call has been booked! Check your email for confirmation.'))
                ctx['booking'] = bk
                return render(request, 'core/booking_success.html', ctx)
    else:
        form = BookingForm()

    # Build available time slots for JS
    slots_by_day = {}
    for slot in available_slots:
        day = slot.day_of_week
        if day not in slots_by_day:
            slots_by_day[day] = []
        slots_by_day[day].append({
            'start': slot.start_time.strftime('%H:%M'),
            'end': slot.end_time.strftime('%H:%M'),
        })

    # Get already booked slots for the next 60 days
    today = datetime.date.today()
    booked = Booking.objects.filter(
        date__gte=today,
        date__lte=today + datetime.timedelta(days=60),
    ).exclude(status='cancelled').values_list('date', 'time_slot')
    booked_json = [
        {'date': d.isoformat(), 'time': t.strftime('%H:%M')}
        for d, t in booked
    ]

    ctx.update({
        'form': form,
        'slots_by_day_json': json.dumps(slots_by_day),
        'booked_slots_json': json.dumps(booked_json),
    })
    return render(request, 'core/booking.html', ctx)


def lead_magnet(request):
    """Lead magnet download page with double opt-in."""
    ctx = _get_common_context()

    if request.method == 'POST':
        form = SubscriberForm(request.POST)

        # Honeypot check
        if form.is_valid() and form.cleaned_data.get('website_url'):
            messages.success(request, _('Thank you! Check your email to confirm.'))
            return redirect('core:lead_magnet')

        if form.is_valid():
            email = form.cleaned_data['email']
            import secrets
            from django.utils import timezone as tz

            # Update or create subscriber
            sub, created = Subscriber.objects.get_or_create(
                email=email,
                defaults={
                    'name': form.cleaned_data.get('name', ''),
                    'consent': form.cleaned_data['consent'],
                    'lead_magnet': 'checklist',
                    'source_page': request.META.get('HTTP_REFERER', ''),
                    'status': 'pending',
                    'confirmation_token': secrets.token_urlsafe(32),
                    'token_created_at': tz.now(),
                }
            )

            if not created:
                if sub.status == 'confirmed':
                    # Already confirmed — show download directly
                    ctx['download_ready'] = True
                    ctx['form'] = SubscriberForm()
                    messages.success(request, _('You are already confirmed! Download your checklist below.'))
                    return render(request, 'core/lead_magnet.html', ctx)
                # Re-send confirmation for pending/unsubscribed
                sub.confirmation_token = secrets.token_urlsafe(32)
                sub.token_created_at = tz.now()
                sub.status = 'pending'
                sub.consent = form.cleaned_data['consent']
                sub.save(update_fields=['consent', 'status', 'confirmation_token', 'token_created_at'])

            # Send confirmation email with token link
            try:
                from django.core.mail import EmailMultiAlternatives
                from django.conf import settings

                site_url = getattr(settings, 'SITE_URL', 'https://getnexiro.com')
                confirm_url = f"{site_url}/{(get_language() or 'en')}/confirm/{sub.confirmation_token}/"

                user_lang = getattr(request, 'LANGUAGE_CODE', None) or 'en'
                if user_lang.startswith('fr'):
                    visitor_subject = "Confirmez votre e-mail — getNexiro"
                    visitor_body = (
                        f"Bonjour {sub.name or ''},\n\n"
                        f"Veuillez confirmer votre adresse e-mail pour télécharger la Checklist de Lancement de Site Web :\n\n"
                        f"{confirm_url}\n\n"
                        f"Ce lien expire dans 48 heures.\n\n"
                        f"Si vous n'avez pas demandé ce téléchargement, vous pouvez ignorer cet e-mail en toute sécurité.\n\n"
                        f"Cordialement,\nL'équipe getNexiro\n"
                    )
                elif user_lang.startswith('ar'):
                    visitor_subject = "تأكيد بريدك الإلكتروني — getNexiro"
                    visitor_body = (
                        f"مرحباً {sub.name or ''}،\n\n"
                        f"يرجى تأكيد بريدك الإلكتروني لتحميل قائمة مراجعة إطلاق المواقع الإلكترونية المجانية:\n\n"
                        f"{confirm_url}\n\n"
                        f"تنتهي صلاحية هذا الرابط بعد 48 ساعة.\n\n"
                        f"إذا لم تكن قد طلبت هذا التحميل، يمكنك تجاهل هذه الرسالة بأمان.\n\n"
                        f"مع خالص التحية،\nفريق getNexiro\n"
                    )
                else:
                    visitor_subject = "Confirm your email — getNexiro"
                    visitor_body = (
                        f"Hi {sub.name or 'there'},\n\n"
                        f"Please confirm your email address to download the Website Launch Checklist:\n\n"
                        f"{confirm_url}\n\n"
                        f"This link expires in 48 hours.\n\n"
                        f"If you did not request this, you can safely ignore this email.\n\n"
                        f"Best regards,\nThe getNexiro Team\n"
                    )

                visitor_email = EmailMultiAlternatives(
                    subject=visitor_subject,
                    body=visitor_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                )
                visitor_email.extra_headers['Auto-Submitted'] = 'auto-replied'
                visitor_email.extra_headers['X-Auto-Response-Suppress'] = 'All'
                visitor_email.extra_headers['Precedence'] = 'auto_reply'
                visitor_email.send(fail_silently=True)
            except Exception:
                pass

            messages.success(request, _('Check your email to confirm and get your download link!'))
            ctx['form'] = SubscriberForm()
            return render(request, 'core/lead_magnet.html', ctx)
    else:
        form = SubscriberForm()

    ctx['form'] = form
    return render(request, 'core/lead_magnet.html', ctx)


def confirm_subscription(request, token):
    """Confirm a subscriber's email via token. Reveal PDF download link."""
    from django.utils import timezone as tz
    ctx = _get_common_context()

    try:
        sub = Subscriber.objects.get(confirmation_token=token)
    except Subscriber.DoesNotExist:
        messages.error(request, _('Invalid or expired confirmation link. Please try subscribing again.'))
        return redirect('core:lead_magnet')

    # Check token expiry (48 hours)
    if sub.token_created_at and (tz.now() - sub.token_created_at).total_seconds() > 48 * 3600:
        messages.error(request, _('This confirmation link has expired. Please subscribe again to receive a new link.'))
        return redirect('core:lead_magnet')

    # Confirm the subscriber
    sub.status = 'confirmed'
    sub.confirmation_token = ''  # Clear token after use
    sub.save(update_fields=['status', 'confirmation_token'])

    messages.success(request, _('Email confirmed! You can now download your checklist.'))
    ctx['download_ready'] = True
    ctx['confirmed'] = True
    ctx['form'] = SubscriberForm()
    return render(request, 'core/lead_magnet.html', ctx)





def city_service_page(request, service_slug, city_slug):
    """Service x City landing page for local SEO."""
    ctx = _get_common_context()
    page = get_object_or_404(
        CityServicePage.objects.select_related('service'),
        slug=city_slug, service__slug=service_slug, is_published=True
    )

    # Get other city pages for this service (for internal linking)
    other_cities = CityServicePage.objects.filter(
        service=page.service, is_published=True
    ).exclude(pk=page.pk)

    ctx.update({
        'page': page,
        'service': page.service,
        'other_cities': other_cities,
        'breadcrumbs': [
            {'name': _('Home'), 'url': reverse('core:home')},
            {'name': _('Services'), 'url': reverse('core:services')},
            {'name': page.service.title, 'url': reverse('core:service_detail', kwargs={'slug': page.service.slug})},
            {'name': page.h1, 'url': request.path},
        ],
    })
    return render(request, 'core/city_service_page.html', ctx)


def blog_rss_feed(request):
    """RSS 2.0 feed per language for blog posts."""
    from django.utils.feedgenerator import Rss201rev2Feed
    from django.conf import settings

    lang = get_language() or 'en'
    site_url = getattr(settings, 'SITE_URL', 'https://getnexiro.com')
    config = SiteConfig.load()

    feed = Rss201rev2Feed(
        title=f'{config.site_name} Blog',
        link=f'{site_url}/{lang}/blog/',
        description=str(_('Expert insights on web development, mobile apps, and digital transformation.')),
        language=lang,
    )

    posts = BlogPost.objects.filter(status='published').order_by('-published_at')[:20]
    for post in posts:
        feed.add_item(
            title=post.title,
            link=f'{site_url}/{lang}/blog/{post.slug}/',
            description=post.excerpt or post.body[:300],
            author_name=post.author_name,
            pubdate=post.published_at,
            updateddate=post.updated_at,
            categories=[post.category.name] if post.category else [],
        )

    response = feed.writeString('utf-8')
    return __import__('django.http', fromlist=['HttpResponse']).HttpResponse(
        response, content_type='application/rss+xml; charset=utf-8'
    )


def blog_category_archive(request, slug):
    """Blog posts filtered by category."""
    ctx = _get_common_context()
    category = get_object_or_404(BlogCategory, slug=slug)
    posts = BlogPost.objects.filter(status='published', category=category).select_related('category')

    ctx.update({
        'posts': posts,
        'categories': BlogCategory.objects.all(),
        'active_category': slug,
        'archive_title': category.name,
        'archive_type': 'category',
    })
    ctx['page_seo_title'] = f'{category.name} — {_("Blog")}'
    return render(request, 'core/blog.html', ctx)


def blog_tag_archive(request, tag):
    """Blog posts filtered by tag."""
    ctx = _get_common_context()
    posts = BlogPost.objects.filter(
        status='published', tags__icontains=tag
    ).select_related('category')

    ctx.update({
        'posts': posts,
        'categories': BlogCategory.objects.all(),
        'active_tag': tag,
        'archive_title': tag,
        'archive_type': 'tag',
    })
    ctx['page_seo_title'] = f'{tag} — {_("Blog")}'
    return render(request, 'core/blog.html', ctx)


def unsubscribe(request):
    """Handle unsubscribe requests."""
    ctx = _get_common_context()
    email = request.GET.get('email', '')

    if request.method == 'POST':
        email = request.POST.get('email', '')
        try:
            sub = Subscriber.objects.get(email=email)
            sub.status = 'unsubscribed'
            sub.save(update_fields=['status'])
            messages.success(request, _('You have been unsubscribed successfully.'))
        except Subscriber.DoesNotExist:
            messages.info(request, _('Email address not found in our records.'))
        return redirect('core:home')

    ctx['email'] = email
    return render(request, 'core/unsubscribe.html', ctx)


# ── Error Handlers ───────────────────────────────────────────────

def handler404_view(request, exception=None):
    """Custom 404 page in the site's design."""
    ctx = _get_common_context()
    return render(request, 'core/404.html', ctx, status=404)


def handler500_view(request):
    """Custom 500 page in the site's design."""
    # Don't rely on DB for 500 — use minimal context
    ctx = {'config': None}
    try:
        ctx = _get_common_context()
    except Exception:
        pass
    return render(request, 'core/500.html', ctx, status=500)
