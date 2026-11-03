"""
getNexiro — Sitemap and robots.txt views.
Generates 100% accurate multilingual sitemap.xml with hreflang alternates using dynamic reverse.
"""

from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.utils.translation import activate
from core.models import Service, Project, BlogPost, BlogCategory, CityServicePage


def robots_txt(request):
    """Serve robots.txt."""
    site_url = getattr(settings, 'SITE_URL', 'https://getnexiro.com')
    content = f"""User-agent: *
Allow: /

Sitemap: {site_url}/sitemap.xml

# Disallow private and administrative paths
Disallow: /admin/
Disallow: /i18n/
Disallow: */confirm/
Disallow: */unsubscribe/
"""
    return HttpResponse(content, content_type='text/plain')


def sitemap_xml(request):
    """Generate a 100% accurate multilingual sitemap.xml with hreflang alternates."""
    site_url = getattr(settings, 'SITE_URL', 'https://getnexiro.com')
    languages = ['en', 'fr', 'ar']
    now = timezone.now().strftime('%Y-%m-%d')

    urls = []

    def add_entry(view_name, kwargs=None, priority='0.5', changefreq='weekly', lastmod=None):
        if lastmod is None:
            lastmod = now
        alternates = []
        en_url = ''
        for lang in languages:
            activate(lang)
            rel_url = reverse(view_name, kwargs=kwargs)
            full_url = f"{site_url}{rel_url}"
            alternates.append({'lang': lang, 'url': full_url})
            if lang == 'en':
                en_url = full_url

        alternates.append({'lang': 'x-default', 'url': en_url})
        urls.append({
            'loc': en_url,
            'lastmod': lastmod,
            'changefreq': changefreq,
            'priority': priority,
            'alternates': alternates,
        })

    # 1. Static Pages
    static_routes = [
        ('core:home', None, '1.0', 'weekly'),
        ('core:about', None, '0.8', 'monthly'),
        ('core:services', None, '0.9', 'weekly'),
        ('core:projects', None, '0.9', 'weekly'),
        ('core:blog', None, '0.8', 'daily'),
        ('core:blog_rss_feed', None, '0.4', 'daily'),
        ('core:contact', None, '0.8', 'monthly'),
        ('core:packages', None, '0.8', 'monthly'),
        ('core:quote_wizard', None, '0.7', 'monthly'),
        ('core:booking', None, '0.7', 'monthly'),
        ('core:lead_magnet', None, '0.6', 'monthly'),
        ('core:privacy_policy', None, '0.3', 'yearly'),
        ('core:terms_of_service', None, '0.3', 'yearly'),
    ]

    for name, kw, prio, freq in static_routes:
        add_entry(name, kw, prio, freq)

    # 2. Dynamic pages: Services
    for svc in Service.objects.all():
        add_entry('core:service_detail', {'slug': svc.slug}, '0.8', 'monthly')

    # 3. Dynamic pages: Projects
    for prj in Project.objects.all():
        lm = prj.created_at.strftime('%Y-%m-%d') if prj.created_at else now
        add_entry('core:project_detail', {'slug': prj.slug}, '0.7', 'monthly', lastmod=lm)

    # 4. Dynamic pages: Blog categories
    for cat in BlogCategory.objects.all():
        add_entry('core:blog_category_archive', {'slug': cat.slug}, '0.6', 'weekly')

    # 5. Dynamic pages: Blog posts
    for post in BlogPost.objects.filter(status='published'):
        lm = post.updated_at.strftime('%Y-%m-%d') if post.updated_at else now
        add_entry('core:blog_detail', {'slug': post.slug}, '0.7', 'weekly', lastmod=lm)

    # 6. Dynamic pages: City service pages
    for cp in CityServicePage.objects.filter(is_published=True).select_related('service'):
        lm = cp.updated_at.strftime('%Y-%m-%d') if cp.updated_at else now
        add_entry('core:city_service_page', {'service_slug': cp.service.slug, 'city_slug': cp.slug}, '0.8', 'monthly', lastmod=lm)

    # Build XML
    xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    xml_parts.append('        xmlns:xhtml="http://www.w3.org/1999/xhtml">')

    for url_entry in urls:
        xml_parts.append('  <url>')
        xml_parts.append(f'    <loc>{url_entry["loc"]}</loc>')
        xml_parts.append(f'    <lastmod>{url_entry["lastmod"]}</lastmod>')
        xml_parts.append(f'    <changefreq>{url_entry["changefreq"]}</changefreq>')
        xml_parts.append(f'    <priority>{url_entry["priority"]}</priority>')
        for alt in url_entry.get('alternates', []):
            xml_parts.append(f'    <xhtml:link rel="alternate" hreflang="{alt["lang"]}" href="{alt["url"]}" />')
        xml_parts.append('  </url>')

    xml_parts.append('</urlset>')

    return HttpResponse('\n'.join(xml_parts), content_type='application/xml')
