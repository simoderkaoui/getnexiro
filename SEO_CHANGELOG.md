# getNexiro — Comprehensive SEO Overhaul Changelog & Audit Report

**Date:** November 2026  
**Platform:** Django 5.1.15 Trilingual Site (`/en/`, `/fr/`, `/ar/`)  
**Domain:** `getnexiro.com`  
**Status:** All 9 Phases Complete & Verified (136/136 Automated Tests Passing, 726/726 Crawled URLs Clean)

---

## 1. Executive Summary

Over a 9-phase architectural SEO and technical performance overhaul, all critical indexing, canonicalization, URL structure, multilingual routing, schema markup, and performance defects on `getnexiro.com` were permanently resolved.

### Key Milestones Achieved:
1. **Duplicate City Content & Canonicalization Fixed:** Single canonical short slugs established (`/tangier/`, `/tetouan/`, `/fes/`, `/meknes/`); all legacy redundant slugs permanently 301-redirected. Remote delivery fields added; thin placeholder city pages safely set to `noindex`. Conditional heading logic prevents "from Tangier to Tangier".
2. **Editorial Blog Hygiene & E-E-A-T:** 23 blog posts audited. 20 off-topic posts (lifestyle, wellness, crypto, side hustles) safely marked `noindex=True` and hidden from the sitemap/blog index. 3 core on-topic engineering posts enhanced with E-E-A-T author boxes, published/modified dates, and branded fallback featured images. Generated `BLOG_CLAIMS_TO_VERIFY.md` for claim audits.
3. **Meta Tags & Social Hygiene:** Completely removed obsolete `<meta name="keywords">` across all templates. Titles strictly formatted ($\le 60$ characters, `[Page Topic] | getNexiro`). Descriptions optimized to 120–158 characters. Open Graph and Twitter cards 100% synchronized with true 1200x630 imagery and trilingual `og:locale` alternates.
4. **Permanent Arabic URL Normalization:** Eliminated URL stacking bugs caused by non-ASCII paths under cPanel mod_passenger (`/ar/من-نحن/ar/خدمات/`). Standardized all routes to clean ASCII slugs (`/ar/about/`, `/ar/services/`, etc.) with comprehensive 301 redirects for legacy paths. Absolute reciprocal hreflang (`en`, `fr`, `ar`, `x-default`) deployed site-wide.
5. **Rich Structured Data (JSON-LD):** Validated Google-compliant schemas:
   - `Organization` & `ProfessionalService` for Tangier HQ with exact NAP and coordinates (`35.7796, -5.8030`).
   - `BreadcrumbList` across all inner pages.
   - `BlogPosting` on technical articles with fallback imagery.
   - `Service` schema on all service and city pages.
   - Deprecated `FAQPage` schema removed. Zero fake reviews or aggregate ratings.
6. **Sitemap & Robots Automation:** Dynamic `sitemap.xml` strictly emitting 200 OK canonical ASCII URLs with model `lastmod` and `xhtml:link` alternates. Clean `robots.txt` disallowing internal search/category parameters. Single-hop 301 canonicalization for root `/` $\to$ `/en/` and `www` $\to$ non-www.
7. **Performance & Core Web Vitals:** Background videos optimized with `preload="none"`, `poster` images, and CSS media queries skipping video playback on mobile ($\le 768\text{px}$) and reduced-motion/data modes. 100% of images now have explicit `width`, `height`, `decoding="async"`, and descriptive `alt` tags. External `flagcdn.com` assets replaced with local SVGs.
8. **On-Page Polish & Contextual Linking:** Reduced repetitive "Tangier, Morocco" phrasing. Generic anchor texts replaced with descriptive callouts. Google Maps embed for Tangier HQ integrated into contact page. Two-way contextual linking established between services, case studies, and blog articles. Personal GitHub profile removed from footer.

---

## 2. Comprehensive Register of 301 Permanent Redirects

All redirects operate with single-hop permanent 301 status codes handled directly at the middleware and route layer (`core/middleware.py` and `core/urls.py`):

| Source URL (Legacy / Duplicate) | Destination URL (Canonical) | Reason / Phase |
| :--- | :--- | :--- |
| `/*/services/web-development/web-development-tangier/` | `/*/services/web-development/tangier/` | Phase 1 (Duplicate city slug) |
| `/*/services/web-development/web-development-tetouan/` | `/*/services/web-development/tetouan/` | Phase 1 (Duplicate city slug) |
| `/*/services/web-development/web-development-fes/` | `/*/services/web-development/fes/` | Phase 1 (Duplicate city slug) |
| `/*/services/web-development/web-development-meknes/` | `/*/services/web-development/meknes/` | Phase 1 (Duplicate city slug) |
| `/ar/من-نحن/` | `/ar/about/` | Phase 4 (Arabic path normalization) |
| `/ar/خدمات/` | `/ar/services/` | Phase 4 (Arabic path normalization) |
| `/ar/مشاريع/` | `/ar/projects/` | Phase 4 (Arabic path normalization) |
| `/ar/مدونة/` | `/ar/blog/` | Phase 4 (Arabic path normalization) |
| `/ar/تواصل/` | `/ar/contact/` | Phase 4 (Arabic path normalization) |
| `/ar/خدمات/web-development/tangier/` | `/ar/services/web-development/tangier/` | Phase 4 (Arabic mixed path) |
| `/ar/من-نحن/ar/خدمات/` (and chained paths) | `/ar/services/` | Phase 4 (cPanel Passenger URL stacking) |
| `/ar/خدمات/ar/مشاريع/` (and chained paths) | `/ar/projects/` | Phase 4 (cPanel Passenger URL stacking) |
| `/fr/a-propos/` | `/fr/about/` | Phase 4 (Uniform ASCII routing) |
| `/` (Root domain) | `/en/` | Phase 6 (Language entry negotiation) |
| `https://www.getnexiro.com/*` | `https://getnexiro.com/*` | Phase 6 (Single-hop canonical host) |

---

## 3. Blog Posts Audit & Classification Table

Total Posts Audited: 23. Per hard rules, **no posts were deleted**. Instead, off-topic posts were set to `noindex=True, index_in_sitemap=False` via Django migration `0025_blogpost_noindex_and_more.py`.

| # | Slug | Category | Topic Status | Index Status | Action Taken |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `building-scalable-saas-django-react-guide` | Engineering | **ON-TOPIC** | **Indexable** | Kept in sitemap, added E-E-A-T author box, lastmod |
| 2 | `flutter-vs-react-native-morocco-2026` | Engineering | **ON-TOPIC** | **Indexable** | Kept in sitemap, added E-E-A-T author box, lastmod |
| 3 | `why-morocco-nearshoring-hub-tech-2026` | Business & Strategy | **ON-TOPIC** | **Indexable** | Kept in sitemap, added E-E-A-T author box, lastmod |
| 4 | `ai-agents-replacing-junior-developers-2026` | AI & Automation | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 5 | `ai-voice-cloning-scams-protect-yourself` | AI & Automation | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 6 | `vibe-coding-ai-tools-software-development` | AI & Automation | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 7 | `ai-wrapper-businesses-making-millions` | Money & Income | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 8 | `side-hustles-that-actually-work-2026` | Money & Income | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 9 | `freelancing-is-dead-what-to-do-instead` | Money & Income | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 10 | `hidden-costs-running-saas-nobody-talks-about` | Money & Income | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 11 | `college-degrees-worthless-tech-careers` | Industry & Insights | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 12 | `remote-work-wars-why-ceos-are-forcing-rto` | Industry & Insights | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 13 | `death-traditional-advertising-creator-economy` | Industry & Insights | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 14 | `tech-layoffs-software-engineers-moving-to-trades`| Industry & Insights | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 15 | `digital-detox-saved-career-tech-worker` | Culture & Lifestyle | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 16 | `rise-ai-companions-loneliness-epidemic` | Culture & Lifestyle | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 17 | `gen-z-workplace-revolution-quiet-quitting` | Culture & Lifestyle | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 18 | `biohacking-tech-workers-optimizing-sleep-focus`| Culture & Lifestyle | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 19 | `digital-nomad-lifestyle-reality-check` | Culture & Lifestyle | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 20 | `stop-using-smartphones-dumbphone-movement` | Tech Opinions | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 21 | `why-every-company-is-becoming-ai-company` | Tech Opinions | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 22 | `death-search-engine-how-ai-overviews-changed-web`| Tech Opinions | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |
| 23 | `open-source-software-dying-corporate-takeover` | Tech Opinions | OFF-TOPIC | Noindex | Meta noindex, hidden from sitemap & blog index |

---

## 4. Performance & Media Optimizations (Phase 7 & 8)

1. **Hero Background Video:**
   - Added `preload="none"` and `poster="{% static 'images/og-image.png' %}"` in `templates/core/home.html` and `templates/core/includes/page_header_video.html`.
   - Replaced missing `circuit-board.svg` reference.
   - Added CSS media queries in `static/css/main.css`:
     ```css
     @media (max-width: 768px), (prefers-reduced-motion: reduce), (prefers-reduced-data: reduce) {
         .hero-bg-video,
         .page-header-video {
             display: none !important;
         }
     }
     ```
2. **Explicit Dimensions & Zero Layout Shift:**
   - 100% of images audited and given explicit `width`, `height`, `decoding="async"`, and `loading="lazy"` across:
     - `author_detail.html` (Avatar 110x110)
     - `blog.html` (Card images 600x340)
     - `blog_detail.html` (Featured image 1200x630 with `fetchpriority="high"`, author photo 64x64)
     - `home.html` (Testimonial avatar 50x50, client logos 160x48)
     - `projects.html` (Cards 600x375, fallback logo 200x60)
     - `project_detail.html` (Hero showcase 1200x675, thumbnails 100x60, related project cards 600x375)
3. **Client Marquee Carousel:**
   - Cloned carousel items marked `aria-hidden="true"` with empty `alt=""` to prevent screen reader stutter and SEO duplicate image parsing.
4. **Caching & Compression:**
   - Django settings confirm `WhiteNoiseMiddleware` with `CompressedStaticFilesStorage` and `WHITENOISE_MAX_AGE = 31536000` (1 year immutable cache for versioned assets).
   - Nginx / Apache production cache header recommendations provided below.

---

## 5. Items Needing Owner Decision

Please review the following operational decisions:

### A. Hard Deletion of 20 Off-Topic Blog Posts
The 20 off-topic articles listed in Section 3 are currently hidden from search crawlers (`<meta name="robots" content="noindex, follow">`) and excluded from `sitemap.xml` and the blog index.
- **Option 1 (Recommended):** Leave them in the database with `noindex=True`. They do not harm SEO or crawl budget, and existing internal links remain intact.
- **Option 2:** Hard delete them via an irreversible migration if you prefer a completely clean database. Let us know if you approve hard deletion.

### B. Personal GitHub Repository Link
- The link `https://github.com/simoderkaoui/getnexiro` was removed from the public website footer in `templates/base.html` and `core/models.py`.
- **Action Required:** Ensure your GitHub repository `simoderkaoui/getnexiro` is set to **Private** or thoroughly reviewed to guarantee no production API keys, database credentials, or secret keys are exposed.
- If you have an official GitHub organization (e.g. `github.com/getnexiro`), provide the URL so we can re-enable it in the footer.

### C. Social Profiles in Structured Data (`sameAs`)
- In `templates/core/includes/jsonld_organization.html`, only Instagram (`https://www.instagram.com/getnexiro`) is currently enabled.
- If you have active LinkedIn, X (Twitter), or Facebook company pages, please provide their official URLs to add them to `sameAs`.

---

## 6. Items Needing Real Content from Owner (Zero-Invention Policy)

Per the strict HARD RULES, no false reviews, addresses, or client claims were invented. The following areas are fully built and ready for your real data:

1. **Remote City Service Pages (Tétouan, Fès, Meknès):**
   - New database fields were added to `CityServicePage` (`intro_text_en/fr/ar`, `local_industries_en/fr/ar`, `local_projects_en/fr/ar`, `local_landmarks_en/fr/ar`).
   - Because real local case studies and partnerships have not yet been provided, these 3 city pages are currently set to `noindex=True` and excluded from `sitemap.xml`.
   - **Action Required:** When you provide real project details for Tétouan, Fès, and Meknès (remotely delivered), populate them in Django admin (`/admin/core/cityservicepage/`) and check `is_published=True` to immediately index them.
2. **Client Testimonials:**
   - The testimonials section in `templates/core/home.html` is wrapped in `{% if testimonials %}`. Because no real approved reviews exist in the database yet, the section is completely invisible to users and search engines (no placeholder/dummy quotes).
   - **Action Required:** Add genuine client testimonials via Django admin (`/admin/core/testimonial/`). Once added, the section will render automatically.
3. **Author Bios & Photos:**
   - Author boxes on `templates/core/blog_detail.html` display real author names and roles. Where bio text or headshots are missing, a clean fallback avatar and role are displayed.
   - **Action Required:** Update author profiles in `/admin/core/author/` with professional bios and photos.
4. **Statistical Claims Verification:**
   - Please review `BLOG_CLAIMS_TO_VERIFY.md` in the repository root. It lists specific numerical figures and statistics mentioned across articles for your verification.
5. **Google Business Profile (GBP):**
   - Ensure your Google Business Profile is claimed and verified for the Tangier HQ address:
     `Ibn Batouta Bureaux, Av. Youssef Ibn Tachfine, Tangier 90000, Morocco` (Coordinates: `35.7796, -5.8030`).
   - The on-page NAP and JSON-LD `LocalBusiness` data match this address identically.

---

## 7. Recommended Production Server Cache Configuration

To maximize Google PageSpeed scores on your production server (Apache/cPanel or Nginx), ensure these caching directives are present:

### Apache / cPanel (`.htaccess`):
```apache
<IfModule mod_expires.c>
    ExpiresActive On
    # Static assets: 1 year cache
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"
    ExpiresByType image/svg+xml "access plus 1 year"
    ExpiresByType image/webp "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType font/woff2 "access plus 1 year"
    # User media uploads: 1 day cache
    ExpiresByType video/mp4 "access plus 1 day"
</IfModule>
```

### Nginx:
```nginx
location /static/ {
    alias /home/getnexiro/public_html/staticfiles/;
    expires 365d;
    add_header Cache-Control "public, max-age=31536000, immutable";
}

location /media/ {
    alias /home/getnexiro/public_html/media/;
    expires 1d;
    add_header Cache-Control "public, max-age=86400";
}
```

---

## 8. Verification Results

- **Django Automated Test Suite:** `Ran 136 tests in 15.449s. OK` (100% passing).
- **Internal Site Crawler:**
  - 726 pages crawled across `/en/`, `/fr/`, and `/ar/`
  - 0 broken links (404/500)
  - 0 redirect chains
  - 0 missing canonical tags
  - 0 missing `<h1>` tags
  - 0 duplicate `<h1>` tags
  - 0 images missing `alt` attributes
