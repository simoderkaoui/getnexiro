import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse
from core.models import Service, CityServicePage, Project, BlogPost


class Command(BaseCommand):
    help = 'Crawls internal site pages to check for broken links and orphan pages.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting internal link crawler..."))
        client = Client()

        from django.utils import translation

        visited = set()
        to_visit = set()

        # Seed with canonical reversed URLs across all languages
        named_views = ['core:home', 'core:about', 'core:services', 'core:projects', 'core:blog', 'core:contact']
        for lang in ('en', 'fr', 'ar'):
            translation.activate(lang)
            for v_name in named_views:
                try:
                    to_visit.add(reverse(v_name))
                except Exception:
                    pass
        translation.activate('en')

        inbound_links = {}
        broken_links = []
        crawled_statuses = {}

        while to_visit:
            current_url = to_visit.pop()
            if current_url in visited:
                continue
            visited.add(current_url)

            try:
                res = client.get(current_url, follow=False)
                status_code = res.status_code
                crawled_statuses[current_url] = status_code

                if status_code in (301, 302):
                    # Redirects are acceptable, but log if broken redirect
                    target = res.headers.get('Location', '')
                    if target and target.startswith('/'):
                        if target not in visited:
                            to_visit.add(target)
                    continue

                if status_code != 200:
                    broken_links.append((current_url, status_code, "Direct Crawl"))
                    continue

                content_type = res.headers.get('Content-Type', '')
                if 'text/html' not in content_type:
                    continue

                soup = BeautifulSoup(res.content.decode('utf-8', errors='ignore'), 'html.parser')
                anchors = soup.find_all('a', href=True)

                for a in anchors:
                    raw_href = a['href'].strip()
                    if not raw_href or raw_href.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'whatsapp:')):
                        continue
                    if 'wa.me' in raw_href or 'twitter.com' in raw_href or 'linkedin.com' in raw_href:
                        continue

                    # Parse URL
                    parsed = urlparse(raw_href)
                    if parsed.netloc and parsed.netloc not in ('getnexiro.com', 'testserver'):
                        continue

                    path = parsed.path
                    if not path.startswith('/'):
                        path = urljoin(current_url, path)

                    # Strip trailing fragment / queries for indexable internal crawl
                    clean_path = path

                    # Track inbound links
                    inbound_links.setdefault(clean_path, set()).add(current_url)

                    # Only queue internal html routes
                    if clean_path.startswith(('/en/', '/fr/', '/ar/')):
                        if clean_path not in visited and clean_path not in to_visit:
                            to_visit.add(clean_path)

            except Exception as e:
                broken_links.append((current_url, str(e), "Exception"))

        self.stdout.write(self.style.SUCCESS(f"Total pages crawled: {len(visited)}"))

        # Verify inbound status of all discovered internal links
        for internal_path, sources in inbound_links.items():
            if internal_path.startswith(('/en/', '/fr/', '/ar/')) and internal_path not in crawled_statuses:
                try:
                    resp = client.get(internal_path, follow=False)
                    crawled_statuses[internal_path] = resp.status_code
                    if resp.status_code == 404:
                        for src in list(sources)[:3]:
                            broken_links.append((src, internal_path, f"404 Not Found"))
                except Exception as ex:
                    broken_links.append((list(sources)[0], internal_path, str(ex)))

        # Check for orphan models/pages using proper reverse per language
        orphan_pages = []
        for service in Service.objects.all():
            for lang in ('en', 'fr', 'ar'):
                translation.activate(lang)
                try:
                    s_url = reverse('core:service_detail', kwargs={'slug': service.slug})
                    if inbound_links.get(s_url) is None and crawled_statuses.get(s_url) != 200:
                        orphan_pages.append(s_url)
                except Exception:
                    pass

        for city_page in CityServicePage.objects.filter(is_published=True):
            for lang in ('en', 'fr', 'ar'):
                translation.activate(lang)
                try:
                    c_url = reverse('core:city_service_page', kwargs={'service_slug': city_page.service.slug, 'city_slug': city_page.slug})
                    if inbound_links.get(c_url) is None and crawled_statuses.get(c_url) != 200:
                        orphan_pages.append(c_url)
                except Exception:
                    pass

        for post in BlogPost.objects.filter(status='published', noindex=False):
            for lang in ('en', 'fr', 'ar'):
                translation.activate(lang)
                try:
                    b_url = reverse('core:blog_detail', kwargs={'slug': post.slug})
                    if inbound_links.get(b_url) is None and crawled_statuses.get(b_url) != 200:
                        orphan_pages.append(b_url)
                except Exception:
                    pass
        translation.activate('en')

        self.stdout.write("=" * 60)
        self.stdout.write(f"CRAWL SUMMARY:")
        self.stdout.write(f"• Total internal URLs crawled: {len(crawled_statuses)}")
        self.stdout.write(f"• Broken internal links: {len(broken_links)}")
        if broken_links:
            self.stdout.write(self.style.ERROR("Broken links found:"))
            for src, target, err in broken_links:
                self.stdout.write(f"  Source: {src} -> Target: {target} ({err})")
        else:
            self.stdout.write(self.style.SUCCESS("✓ No broken internal links found!"))

        self.stdout.write(f"• Orphan indexable pages: {len(orphan_pages)}")
        if orphan_pages:
            self.stdout.write(self.style.WARNING("Orphan pages found:"))
            for orphan in orphan_pages:
                self.stdout.write(f"  {orphan}")
        else:
            self.stdout.write(self.style.SUCCESS("✓ No orphan indexable pages found!"))
        self.stdout.write("=" * 60)
