"""
getNexiro — Sitemap and robots.txt views.
"""

from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from django.conf import settings
from core.models import Service, Project, BlogPost, BlogCategory, CityServicePage


def robots_txt(request):
    """Serve robots.txt."""
    site_url = getattr(settings, 'SITE_URL', 'https://getnexiro.com')
    content = f"""User-agent: *
Allow: /

Sitemap: {site_url}/sitemap.xml

# Disallow admin and private paths
Disallow: /admin/
Disallow: /i18n/
"""
    return HttpResponse(content, content_type='text/plain')


def sitemap_xml(request):
    """Generate a multilingual sitemap.xml with hreflang alternates."""
    site_url = getattr(settings, 'SITE_URL', 'https://getnexiro.com')
    languages = ['en', 'fr', 'ar']
    now = timezone.now().strftime('%Y-%m-%d')

    # Static pages with their URL names
    static_pages = [
        ('', '1.0'),       # Home
        ('about/', '0.8'),
        ('services/', '0.9'),
        ('projects/', '0.9'),
        ('blog/', '0.8'),
        ('contact/', '0.8'),
        ('packages/', '0.8'),
        ('quote/', '0.7'),
        ('booking/', '0.7'),
        ('checklist/', '0.6'),
        ('blog/feed/', '0.3'),
        ('privacy-policy/', '0.3'),
        ('terms-of-service/', '0.3'),
    ]

    urls = []

    # Static pages with hreflang alternates
    for path, priority in static_pages:
        alternates = []
        for lang in languages:
            alternates.append({
                'lang': lang,
                'url': f'{site_url}/{lang}/{path}',
            })
        alternates.append({
            'lang': 'x-default',
            'url': f'{site_url}/en/{path}',
        })
        urls.append({
            'loc': f'{site_url}/en/{path}',
            'lastmod': now,
            'changefreq': 'weekly',
            'priority': priority,
            'alternates': alternates,
        })

    # Dynamic pages: Services
    for service in Service.objects.all():
        alternates = []
        for lang in languages:
            alternates.append({
                'lang': lang,
                'url': f'{site_url}/{lang}/services/{service.slug}/',
            })
        urls.append({
            'loc': f'{site_url}/en/services/{service.slug}/',
            'lastmod': now,
            'changefreq': 'monthly',
            'priority': '0.7',
            'alternates': alternates,
        })

    # Dynamic pages: Projects
    for project in Project.objects.all():
        alternates = []
        for lang in languages:
            alternates.append({
                'lang': lang,
                'url': f'{site_url}/{lang}/projects/{project.slug}/',
            })
        urls.append({
            'loc': f'{site_url}/en/projects/{project.slug}/',
            'lastmod': project.created_at.strftime('%Y-%m-%d') if project.created_at else now,
            'changefreq': 'monthly',
            'priority': '0.7',
            'alternates': alternates,
        })

    # Dynamic pages: Blog posts
    for post in BlogPost.objects.filter(status='published'):
        alternates = []
        for lang in languages:
            alternates.append({
                'lang': lang,
                'url': f'{site_url}/{lang}/blog/{post.slug}/',
            })
        urls.append({
            'loc': f'{site_url}/en/blog/{post.slug}/',
            'lastmod': post.updated_at.strftime('%Y-%m-%d') if post.updated_at else now,
            'changefreq': 'weekly',
            'priority': '0.6',
            'alternates': alternates,
        })


    # Dynamic pages: Blog categories
    for cat in BlogCategory.objects.all():
        alternates = []
        for lang in languages:
            alternates.append({
                'lang': lang,
                'url': f'{site_url}/{lang}/blog/category/{cat.slug}/',
            })
        urls.append({
            'loc': f'{site_url}/en/blog/category/{cat.slug}/',
            'lastmod': now,
            'changefreq': 'weekly',
            'priority': '0.5',
            'alternates': alternates,
        })


    # Dynamic pages: City service pages
    for page in CityServicePage.objects.filter(is_published=True).select_related('service'):
        alternates = []
        for lang in languages:
            alternates.append({
                'lang': lang,
                'url': f'{site_url}/{lang}/services/{page.service.slug}/{page.slug}/',
            })
        urls.append({
            'loc': f'{site_url}/en/services/{page.service.slug}/{page.slug}/',
            'lastmod': page.updated_at.strftime('%Y-%m-%d') if page.updated_at else now,
            'changefreq': 'monthly',
            'priority': '0.6',
            'alternates': alternates,
        })

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
