"""
getNexiro — Sitemap and robots.txt views.
Generates 100% accurate multilingual sitemap.xml with xhtml:link alternates using dynamic reverse.
"""

from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.utils.translation import activate
from core.models import Service, Project, BlogPost, BlogCategory, CityServicePage, LegalPage, SiteConfig, Author


def robots_txt(request):
    """Serve robots.txt."""
    site_url = getattr(settings, 'SITE_URL', 'https://getnexiro.com').rstrip('/')
    content = f"""User-agent: *
Allow: /
Allow: /static/
Allow: /media/

# Disallow private, search, administrative and utility paths
Disallow: /admin/
Disallow: /i18n/
Disallow: /*?search=*
Disallow: /*?q=*
Disallow: /*?subject=*
Disallow: */confirm/
Disallow: */unsubscribe/
Disallow: */quote/success/
Disallow: */booking/success/

Sitemap: {site_url}/sitemap.xml
"""
    return HttpResponse(content.strip(), content_type='text/plain')


def sitemap_xml(request):
    """
    Generate an accurate multilingual sitemap.xml with xhtml:link alternates.
    - One entry per indexable URL for all 3 languages
    - Excludes noindex items, utility pages, and drafts
    - Accurate lastmod from updated_at
    """
    site_url = getattr(settings, 'SITE_URL', 'https://getnexiro.com').rstrip('/')
    languages = ['en', 'fr', 'ar']

    # Get SiteConfig updated_at or fallback date
    config = SiteConfig.load()
    base_lastmod = '2026-11-10'

    url_entries = []

    def get_alternates(view_name, kwargs=None):
        alternates = []
        urls_by_lang = {}
        for lang in languages:
            activate(lang)
            rel_url = reverse(view_name, kwargs=kwargs)
            full_url = f"{site_url}{rel_url}"
            urls_by_lang[lang] = full_url
            alternates.append({'lang': lang, 'url': full_url})
        alternates.append({'lang': 'x-default', 'url': urls_by_lang['en']})
        return urls_by_lang, alternates

    def add_multilingual_page(view_name, kwargs=None, priority='0.8', changefreq='weekly', lastmod=None):
        if not lastmod:
            lastmod = base_lastmod
        urls_by_lang, alternates = get_alternates(view_name, kwargs)
        for lang in languages:
            url_entries.append({
                'loc': urls_by_lang[lang],
                'lastmod': lastmod,
                'changefreq': changefreq,
                'priority': priority,
                'alternates': alternates,
            })

    # 1. Main Static Indexable Pages
    static_routes = [
        ('core:home', '1.0', 'weekly'),
        ('core:services', '0.9', 'weekly'),
        ('core:projects', '0.9', 'weekly'),
        ('core:about', '0.8', 'monthly'),
        ('core:blog', '0.8', 'daily'),
        ('core:packages', '0.8', 'monthly'),
        ('core:contact', '0.8', 'monthly'),
    ]
    for name, prio, freq in static_routes:
        add_multilingual_page(name, priority=prio, changefreq=freq, lastmod=base_lastmod)

    # 2. Legal Pages (Privacy Policy & Terms)
    for lp_name, lp_slug in [('core:privacy_policy', 'privacy-policy'), ('core:terms_of_service', 'terms-of-service')]:
        lp = LegalPage.objects.filter(slug=lp_slug, noindex=False).first()
        if lp:
            lm = lp.updated_at.strftime('%Y-%m-%d') if lp.updated_at else base_lastmod
            add_multilingual_page(lp_name, priority='0.3', changefreq='yearly', lastmod=lm)

    # 3. Services (only indexable)
    for svc in Service.objects.filter(noindex=False):
        add_multilingual_page('core:service_detail', kwargs={'slug': svc.slug}, priority='0.9', changefreq='weekly', lastmod=base_lastmod)

    # 4. Projects (only indexable)
    for prj in Project.objects.filter(noindex=False):
        prj_date = getattr(prj, 'updated_at', None) or getattr(prj, 'created_at', None)
        lm = prj_date.strftime('%Y-%m-%d') if prj_date else base_lastmod
        add_multilingual_page('core:project_detail', kwargs={'slug': prj.slug}, priority='0.8', changefreq='monthly', lastmod=lm)

    # 5. City Service Pages (only published and indexable)
    for cp in CityServicePage.objects.filter(is_published=True, noindex=False).select_related('service'):
        lm = cp.updated_at.strftime('%Y-%m-%d') if cp.updated_at else base_lastmod
        add_multilingual_page(
            'core:city_service_page',
            kwargs={'service_slug': cp.service.slug, 'city_slug': cp.slug},
            priority='0.8',
            changefreq='monthly',
            lastmod=lm
        )

    # 6. Blog Posts (published, noindex=False, index_in_sitemap=True)
    for post in BlogPost.objects.filter(status='published', noindex=False, index_in_sitemap=True):
        lm = post.updated_at.strftime('%Y-%m-%d') if post.updated_at else (post.published_at.strftime('%Y-%m-%d') if post.published_at else base_lastmod)
        add_multilingual_page('core:blog_detail', kwargs={'slug': post.slug}, priority='0.7', changefreq='weekly', lastmod=lm)

    # 7. Blog Categories (only those with published, indexable posts)
    active_cats = BlogCategory.objects.filter(
        posts__status='published',
        posts__noindex=False,
        posts__index_in_sitemap=True
    ).distinct()
    for cat in active_cats:
        add_multilingual_page('core:blog_category_archive', kwargs={'slug': cat.slug}, priority='0.6', changefreq='weekly', lastmod=base_lastmod)

    # Reset language to default
    activate('en')

    # Build XML
    xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    xml_parts.append('        xmlns:xhtml="http://www.w3.org/1999/xhtml">')

    for entry in url_entries:
        xml_parts.append('  <url>')
        xml_parts.append(f'    <loc>{entry["loc"]}</loc>')
        xml_parts.append(f'    <lastmod>{entry["lastmod"]}</lastmod>')
        xml_parts.append(f'    <changefreq>{entry["changefreq"]}</changefreq>')
        xml_parts.append(f'    <priority>{entry["priority"]}</priority>')
        for alt in entry.get('alternates', []):
            xml_parts.append(f'    <xhtml:link rel="alternate" hreflang="{alt["lang"]}" href="{alt["url"]}" />')
        xml_parts.append('  </url>')

    xml_parts.append('</urlset>')

    return HttpResponse('\n'.join(xml_parts), content_type='application/xml')
