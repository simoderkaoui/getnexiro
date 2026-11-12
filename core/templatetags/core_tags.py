import re
import urllib.parse
from django import template
from django.conf import settings
from django.utils.translation import get_language, override
from django.urls import resolve, reverse, Resolver404, NoReverseMatch
from django.templatetags.static import static

register = template.Library()

PAGE_CANONICAL_KEYS = {
    'about': 'about', 'a-propos': 'about', 'من-نحن': 'about',
    'services': 'services', 'خدمات': 'services',
    'projects': 'projects', 'projets': 'projects', 'مشاريع': 'projects',
    'blog': 'blog', 'مدونة': 'blog',
    'contact': 'contact', 'تواصل': 'contact',
    'privacy-policy': 'privacy-policy',
    'terms-of-service': 'terms-of-service',
    'quote': 'quote',
    'packages': 'packages',
    'booking': 'booking',
    'checklist': 'checklist',
}

CANONICAL_TARGET_SLUGS = {
    'en': {
        'about': 'about', 'services': 'services', 'projects': 'projects',
        'blog': 'blog', 'contact': 'contact', 'privacy-policy': 'privacy-policy',
        'terms-of-service': 'terms-of-service', 'quote': 'quote',
        'packages': 'packages', 'booking': 'booking', 'checklist': 'checklist',
    },
    'fr': {
        'about': 'a-propos', 'services': 'services', 'projects': 'projets',
        'blog': 'blog', 'contact': 'contact', 'privacy-policy': 'privacy-policy',
        'terms-of-service': 'terms-of-service', 'quote': 'quote',
        'packages': 'packages', 'booking': 'booking', 'checklist': 'checklist',
    },
    'ar': {
        'about': 'من-نحن', 'services': 'خدمات', 'projects': 'مشاريع',
        'blog': 'مدونة', 'contact': 'تواصل', 'privacy-policy': 'privacy-policy',
        'terms-of-service': 'terms-of-service', 'quote': 'quote',
        'packages': 'packages', 'booking': 'booking', 'checklist': 'checklist',
    },
}


@register.filter(name='translate_url')
def translate_url(url, lang_code):
    """
    Given a URL path and a target language code, translate the URL
    to the target language route (e.g. /fr/a-propos/ -> /ar/من-نحن/).
    Cleans duplicate/trailing language codes and falls back gracefully.
    """
    if not url:
        return f'/{lang_code}/'
    try:
        from core.middleware import clean_language_path
        parsed = urllib.parse.urlsplit(str(url))
        cleaned_path = clean_language_path(parsed.path)
        raw_path = urllib.parse.unquote(cleaned_path)
        collapsed = re.sub(r'/+', '/', raw_path)
        parts = [p for p in collapsed.strip('/').split('/') if p]

        if not parts:
            return f'/{lang_code}/'

        known_langs = ('en', 'fr', 'ar')
        if parts[0] in known_langs:
            src_lang = parts[0]
            subparts = parts[1:]
        else:
            src_lang = get_language() or 'en'
            subparts = parts

        # Clean trailing or duplicate language tokens
        while len(subparts) >= 1 and subparts[-1] in known_langs:
            subparts.pop()
        while subparts and subparts[0] in known_langs:
            subparts.pop(0)

        if not subparts:
            qs = f"?{parsed.query}" if parsed.query else ""
            return f"/{lang_code}/{qs}"

        # 1. Try standard Django reverse first with src_lang resolution
        resolved_path = None
        try:
            with override(src_lang):
                test_path = f"/{src_lang}/" + "/".join(subparts) + ("/" if raw_path.endswith('/') else "")
                match = resolve(test_path)
                view_name = f"{match.namespace}:{match.url_name}" if match.namespace else match.url_name
                with override(lang_code):
                    resolved_path = reverse(view_name, args=match.args, kwargs=match.kwargs)
                    resolved_path = urllib.parse.unquote(resolved_path)
        except (Resolver404, NoReverseMatch, Exception):
            pass

        if resolved_path:
            qs = f"?{parsed.query}" if parsed.query else ""
            return f"{resolved_path}{qs}"

        # 2. Fallback to canonical slug table
        first_slug = subparts[0]
        canonical_key = PAGE_CANONICAL_KEYS.get(first_slug)
        if canonical_key:
            target_slug = CANONICAL_TARGET_SLUGS.get(lang_code, {}).get(canonical_key, canonical_key)
            rest = "/" + "/".join(subparts[1:]) if len(subparts) > 1 else ""
            trailing = "/" if raw_path.endswith('/') or not rest else ""
            qs = f"?{parsed.query}" if parsed.query else ""
            return f"/{lang_code}/{target_slug}{rest}{trailing}{qs}"

        return f'/{lang_code}/'
    except Exception:
        return f'/{lang_code}/'


def _format_seo_title(raw_title, default_brand=" | getNexiro"):
    """
    Format and trim title according to SEO rules:
    - Primary keyword first
    - Brand suffix last as ' | getNexiro'
    - Total length <= 60 characters
    """
    if not raw_title:
        return f"Web & App Development in Tangier{default_brand}"

    title = str(raw_title).strip()

    # Remove any existing legacy brand suffixes or redundant tags
    suffixes = [
        "— Web & App Development Agency in Tangier, Morocco",
        "- Web & App Development Agency in Tangier, Morocco",
        " — Web & App Development Agency",
        " | Tangier",
        "— Tangier",
        " | getNexiro",
        "— getNexiro",
        "- getNexiro",
    ]
    for suf in suffixes:
        if title.endswith(suf):
            title = title[:-len(suf)].strip()

    max_len = 60
    brand_len = len(default_brand)
    avail_len = max_len - brand_len
    if len(title) > avail_len:
        title = title[:avail_len].rstrip(' —-|,')
    return f"{title}{default_brand}"


def _format_seo_description(raw_desc, fallback_text=None, lang='en'):
    """
    Format description according to SEO rules:
    - Length strictly between 120 and 155 characters
    - Contains keyword and call to action
    - Never empty
    """
    cta_map = {
        'en': ' Request a free quote today.',
        'fr': ' Demandez votre devis gratuit.',
        'ar': ' اطلب عرض سعر مجاني لمشروعك.',
    }
    cta = cta_map.get(lang, cta_map['en'])

    desc = ''
    if raw_desc:
        desc = re.sub(r'<[^>]+>', ' ', str(raw_desc))
        desc = ' '.join(desc.split()).strip()

    if not desc and fallback_text:
        desc = re.sub(r'<[^>]+>', ' ', str(fallback_text))
        desc = ' '.join(desc.split()).strip()

    if not desc:
        default_descs = {
            'en': 'Premier web and mobile app development agency in Tangier, Morocco. We engineer high-performance platforms for SMBs. Request your free quote today.',
            'fr': 'Agence web et mobile à Tanger au Maroc. Nous concevons des applications performantes pour entreprises. Demandez votre devis gratuit dès aujourd\'hui.',
            'ar': 'وكالة رائدة في تطوير مواقع وتطبيقات الجوال بطنجة والمغرب. تصمم منصات رقمية عالية الأداء للشركات. اطلب عرض سعر مجاني لمشروعك الآن.',
        }
        return default_descs.get(lang, default_descs['en'])

    # Ensure length between 120 and 155 characters
    if len(desc) < 120:
        if not any(call in desc.lower() for call in ['quote', 'contact', 'devis', 'demandez', 'تواصل', 'اطلب']):
            desc = desc.rstrip('. ') + '.' + cta

    if len(desc) < 120:
        padding = {
            'en': ' Scalable software engineering and digital solutions in Tangier, Morocco.',
            'fr': ' Ingénierie logicielle et solutions numériques sur mesure à Tanger, Maroc.',
            'ar': ' حلول برمجية وهندسة رقمية مخصصة للشركات في طنجة، المغرب.',
        }
        desc = desc.rstrip('. ') + '.' + padding.get(lang, padding['en'])

    if len(desc) > 155:
        trimmed = desc[:154].rsplit(' ', 1)[0].rstrip('.,—;-') + '.'
        if len(trimmed) >= 120:
            desc = trimmed
        else:
            desc = desc[:154] + '.'

    return desc


from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


@register.simple_tag(takes_context=True)
def render_seo(context, obj=None, title=None, description=None, image=None, noindex=None, og_type=None):
    """
    Unified SEO inclusion tag:
    - Generates unique <title> <= 60 chars ending in ' | getNexiro'
    - Generates <meta name="description"> between 120-155 chars
    - Generates self-referencing canonical URL (clean without tracking parameters)
    - Generates reciprocal hreflang alternate links + x-default
    - Generates Open Graph & Twitter Card tags with accurate 1200x630 image dimensions
    - Emits robots meta (index/noindex)
    """
    request = context.get('request')
    lang = get_language() or 'en'
    site_url = getattr(settings, 'SITE_URL', 'https://getnexiro.com').rstrip('/')

    # 1. Resolve Object
    if obj is None:
        obj = (
            context.get('post') or
            context.get('service') or
            context.get('project') or
            context.get('page')
        )

    # 2. Determine Title
    raw_title = title or context.get('page_seo_title')
    if not raw_title and obj:
        if hasattr(obj, 'seo_title') and obj.seo_title:
            raw_title = obj.seo_title
        elif hasattr(obj, 'title') and obj.title:
            raw_title = obj.title
        elif hasattr(obj, 'h1') and obj.h1:
            raw_title = obj.h1

    if not raw_title:
        # Fallback by URL name if available
        resolver_match = getattr(request, 'resolver_match', None)
        url_name = getattr(resolver_match, 'url_name', '') if resolver_match else ''
        default_titles = {
            'home': {
                'en': 'Web & App Development Agency in Tangier',
                'fr': 'Agence Web à Tanger — Sites & Applications',
                'ar': 'وكالة تطوير مواقع وتطبيقات بطنجة',
            },
            'about': {
                'en': 'About Our Software Agency in Tangier',
                'fr': 'À Propos de Notre Agence Web à Tanger',
                'ar': 'من نحن — وكالة برمجيات في طنجة',
            },
            'services': {
                'en': 'Custom Software & Web Services',
                'fr': 'Services de Développement Web & Mobile',
                'ar': 'خدمات تطوير البرمجيات والويب',
            },
            'projects': {
                'en': 'Software & Web Development Portfolio',
                'fr': 'Nos Réalisations Web & Applications',
                'ar': 'معرض مشاريعنا وتطبيقاتنا',
            },
            'blog': {
                'en': 'Tech & Software Engineering Insights',
                'fr': 'Blog & Actualités Tech et Ingénierie',
                'ar': 'مدونة التكنولوجيا وهندسة البرمجيات',
            },
            'contact': {
                'en': 'Contact Our Studio in Tangier, Morocco',
                'fr': 'Contactez Notre Agence Web à Tanger',
                'ar': 'تواصل معنا — استشارة تقنية بطنجة',
            },
            'packages': {
                'en': 'Transparent Development Packages',
                'fr': 'Packs de Développement Web Transparents',
                'ar': 'باقات تطوير شفافة للشركات',
            },
        }
        if url_name in default_titles:
            raw_title = default_titles[url_name].get(lang, default_titles[url_name]['en'])
        else:
            raw_title = 'Web & App Development Agency in Tangier'

    final_title = _format_seo_title(raw_title)

    # 3. Determine Description
    raw_desc = description or context.get('page_seo_description')
    fallback_text = None
    if not raw_desc and obj:
        if hasattr(obj, 'seo_description') and obj.seo_description:
            raw_desc = obj.seo_description
        elif hasattr(obj, 'meta_description') and obj.meta_description:
            raw_desc = obj.meta_description
        elif hasattr(obj, 'intro') and obj.intro:
            fallback_text = obj.intro
        elif hasattr(obj, 'excerpt') and obj.excerpt:
            fallback_text = obj.excerpt
        elif hasattr(obj, 'body') and obj.body:
            fallback_text = obj.body[:300]
        elif hasattr(obj, 'description') and obj.description:
            fallback_text = obj.description

    final_description = _format_seo_description(raw_desc, fallback_text=fallback_text, lang=lang)

    # 4. Canonical URL (Strip tracking & non-canonical parameters, auto-clean chained paths)
    from core.middleware import clean_language_path
    clean_path = clean_language_path(request.path) if request else f"/{lang}/"
    if request and 'page' in request.GET:
        page_val = request.GET.get('page')
        if page_val and page_val.isdigit() and int(page_val) > 1:
            clean_path = f"{clean_path}?page={page_val}"

    canonical_url = f"{site_url}{clean_path}"

    # 5. Hreflang Reciprocal Links
    hreflang_alternates = []
    base_request_path = clean_language_path(request.path) if request else '/'
    for alt_lang in ['en', 'fr', 'ar']:
        alt_path = translate_url(base_request_path, alt_lang) or f"/{alt_lang}/"
        hreflang_alternates.append({
            'lang': alt_lang,
            'url': f"{site_url}{alt_path}",
        })
    en_path = translate_url(base_request_path, 'en') or '/en/'
    x_default_url = f"{site_url}{en_path}"

    # 6. Open Graph & Twitter Image
    og_image_url = None
    if image:
        og_image_url = request.build_absolute_uri(image) if request else image
    elif obj:
        img_field = getattr(obj, 'og_image', None) or getattr(obj, 'image', None) or getattr(obj, 'featured_image', None)
        if img_field and hasattr(img_field, 'url'):
            og_image_url = request.build_absolute_uri(img_field.url) if request else img_field.url

    config = context.get('config')
    if not og_image_url and config and getattr(config, 'default_og_image', None):
        og_image_url = request.build_absolute_uri(config.default_og_image.url) if request else config.default_og_image.url

    if not og_image_url:
        og_image_url = f"{site_url}{static('images/og-image.png')}"

    # 7. Locales
    locale_map = {
        'en': 'en_US',
        'fr': 'fr_FR',
        'ar': 'ar_MA',
    }
    og_locale = locale_map.get(lang, 'en_US')
    og_alternate_locales = [v for k, v in locale_map.items() if k != lang]

    # 8. Type
    is_article = False
    if og_type:
        resolved_og_type = og_type
    elif obj and obj.__class__.__name__ == 'BlogPost':
        resolved_og_type = 'article'
        is_article = True
    else:
        resolved_og_type = 'website'

    article_published_time = ''
    article_modified_time = ''
    article_author = ''
    if is_article and obj:
        pub = getattr(obj, 'published_at', None)
        if pub:
            article_published_time = pub.isoformat()
        upd = getattr(obj, 'updated_at', None)
        if upd:
            article_modified_time = upd.isoformat()
        author_obj = getattr(obj, 'author', None)
        if author_obj:
            article_author = author_obj.name
        else:
            article_author = getattr(obj, 'author_name', '') or 'getNexiro'

    # 9. Noindex
    is_noindex = False
    if noindex is not None:
        is_noindex = bool(noindex)
    elif obj and hasattr(obj, 'noindex'):
        is_noindex = bool(obj.noindex)

    seo_data = {
        'seo_title': final_title,
        'seo_description': final_description,
        'canonical_url': canonical_url,
        'hreflang_alternates': hreflang_alternates,
        'x_default_url': x_default_url,
        'og_type': resolved_og_type,
        'og_locale': og_locale,
        'og_alternate_locales': og_alternate_locales,
        'og_image_url': og_image_url,
        'og_image_width': 1200,
        'og_image_height': 630,
        'noindex': is_noindex,
        'article_published_time': article_published_time,
        'article_modified_time': article_modified_time,
        'article_author': article_author,
    }

    rendered_html = render_to_string('core/includes/seo_meta.html', seo_data, request=request)
    return mark_safe(rendered_html)
