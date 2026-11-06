"""
Seed data definitions for 20 viral, high-converting, proof-driven blog posts.
Includes full multilingual content (EN, FR, AR) and automatic luxury dark banner generation.
"""
import os
import textwrap
from pathlib import Path
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.utils import timezone
from core.models import BlogCategory, BlogPost
from core.blog_data import ALL_20_BLOG_POSTS

CATEGORY_COLORS = {
    'ai-automation': ((14, 165, 233), (56, 189, 248)),       # Cyan
    'money-income': ((16, 185, 129), (52, 211, 153)),        # Emerald
    'tech-opinions': ((244, 63, 94), (251, 113, 133)),       # Rose
    'culture-lifestyle': ((168, 85, 247), (192, 132, 252)),  # Purple
    'industry-insights': ((245, 158, 11), (251, 191, 36)),   # Amber
    'engineering': ((14, 165, 233), (56, 189, 248)),
    'design': ((168, 85, 247), (192, 132, 252)),
    'business-strategy': ((245, 158, 11), (251, 191, 36)),
}

def get_font(size, bold=False):
    font_file = 'segoeuib.ttf' if bold else 'segoeui.ttf'
    full_path = f'C:/Windows/Fonts/{font_file}'
    if not os.path.exists(full_path):
        full_path = 'C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf'
    if os.path.exists(full_path):
        try:
            return ImageFont.truetype(full_path, size)
        except Exception:
            pass
    return ImageFont.load_default()

def ensure_blog_banner(slug, category_slug, category_name, title):
    media_dir = Path(settings.MEDIA_ROOT) / 'blog'
    media_dir.mkdir(parents=True, exist_ok=True)
    out_file = media_dir / f"{slug}.jpg"
    rel_path = f"blog/{slug}.jpg"

    if out_file.exists() and out_file.stat().st_size > 1000:
        return rel_path

    try:
        width, height = 1200, 630
        img = Image.new('RGB', (width, height), color=(8, 11, 16))
        draw = ImageDraw.Draw(img)

        primary_col, light_col = CATEGORY_COLORS.get(category_slug, ((14, 165, 233), (56, 189, 248)))

        # Top accent line
        draw.rectangle([0, 0, width, 6], fill=primary_col)

        # Ambient glow
        for r in range(240, 0, -20):
            glow_col = (primary_col[0] // 5, primary_col[1] // 5, primary_col[2] // 5)
            draw.ellipse([920 - r, 120 - r, 920 + r, 120 + r], fill=glow_col)

        # Category Pill
        font_cat = get_font(20, bold=True)
        pill_text = f"•  {category_name.upper()}  •"
        bbox = draw.textbbox((0, 0), pill_text, font=font_cat)
        pill_w = bbox[2] - bbox[0] + 40
        draw.rounded_rectangle([80, 80, 80 + pill_w, 124], radius=22, fill=(15, 23, 42), outline=primary_col, width=2)
        draw.text((100, 91), pill_text, fill=light_col, font=font_cat)

        # Title text
        font_title = get_font(44, bold=True)
        lines = textwrap.wrap(title, width=34)[:4]

        y = 175
        line_height = 58
        for line in lines:
            draw.text((80, y), line, fill=(248, 250, 252), font=font_title)
            y += line_height

        # Decorative line
        draw.line([80, 520, 280, 520], fill=primary_col, width=3)

        # Brand watermark
        font_footer = get_font(20, bold=False)
        draw.text((80, 545), "getNexiro  /  Software Engineering & Digital Studio  —  Tangier, Morocco", fill=(148, 163, 184), font=font_footer)

        img.save(str(out_file), 'JPEG', quality=92, optimize=True)
    except Exception as e:
        print(f"Warning: Failed to generate banner for {slug}: {e}")

    return rel_path

ALL_BLOG_CATEGORIES = [
    {
        'slug': 'ai-automation',
        'name_en': 'AI & Automation',
        'name_fr': 'IA & Automatisation',
        'name_ar': 'الذكاء الاصطناعي والأتمتة',
    },
    {
        'slug': 'money-income',
        'name_en': 'Money & Income',
        'name_fr': 'Finance & Revenus',
        'name_ar': 'المال والدخل',
    },
    {
        'slug': 'tech-opinions',
        'name_en': 'Tech Opinions',
        'name_fr': 'Débats & Opinions',
        'name_ar': 'آراء ونقاشات تقنية',
    },
    {
        'slug': 'culture-lifestyle',
        'name_en': 'Culture & Lifestyle',
        'name_fr': 'Culture & Mode de Vie',
        'name_ar': 'الثقافة ونمط الحياة',
    },
    {
        'slug': 'industry-insights',
        'name_en': 'Industry & Insights',
        'name_fr': 'Industrie & Coulisses',
        'name_ar': 'رؤى محلية وصناعية',
    },
    {
        'slug': 'engineering',
        'name_en': 'Engineering',
        'name_fr': 'Ingénierie',
        'name_ar': 'الهندسة البرمجية',
    },
    {
        'slug': 'design',
        'name_en': 'Design',
        'name_fr': 'Design',
        'name_ar': 'التصميم وتجربة المستخدم',
    },
    {
        'slug': 'business-strategy',
        'name_en': 'Business & Strategy',
        'name_fr': 'Business & Stratégie',
        'name_ar': 'الأعمال والاستراتيجية',
    },
]

def seed_all_blogs(stdout=None):
    category_map = {}
    for cat_data in ALL_BLOG_CATEGORIES:
        cat, created = BlogCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        if not created:
            for k, v in cat_data.items():
                setattr(cat, k, v)
            cat.save()
        category_map[cat.slug] = cat

    now = timezone.now()
    count = 0

    for pdata in ALL_20_BLOG_POSTS:
        slug = pdata['slug']
        cat_slug = pdata['category_slug']
        cat = category_map[cat_slug]

        banner_rel = ensure_blog_banner(slug, cat_slug, cat.name_en, pdata['title_en'])
        days_ago = pdata.get('days_ago', 1)
        pub_date = now - timedelta(days=days_ago)

        fields = {
            'title_en': pdata['title_en'],
            'title_fr': pdata['title_fr'],
            'title_ar': pdata['title_ar'],
            'excerpt_en': pdata['excerpt_en'],
            'excerpt_fr': pdata['excerpt_fr'],
            'excerpt_ar': pdata['excerpt_ar'],
            'body_en': pdata['body_en'],
            'body_fr': pdata['body_fr'],
            'body_ar': pdata['body_ar'],
            'meta_title_en': pdata['meta_title_en'],
            'meta_title_fr': pdata['meta_title_fr'],
            'meta_title_ar': pdata['meta_title_ar'],
            'meta_description_en': pdata['meta_description_en'],
            'meta_description_fr': pdata['meta_description_fr'],
            'meta_description_ar': pdata['meta_description_ar'],
            'meta_keywords': pdata.get('tags', ''),
            'category': cat,
            'author_name': pdata.get('author_name', 'getNexiro Team'),
            'reading_time_minutes': pdata.get('reading_time_minutes', 6),
            'tags': pdata.get('tags', ''),
            'status': 'published',
            'is_featured': pdata.get('is_featured', False),
            'published_at': pub_date,
            'featured_image': banner_rel,
            'featured_image_alt': pdata['title_en'],
        }

        post, created = BlogPost.objects.get_or_create(
            slug=slug,
            defaults=fields
        )
        if not created:
            for k, v in fields.items():
                setattr(post, k, v)
            post.save()
        count += 1

    if stdout:
        stdout.write(f'  [OK] Seeded {count} high-impact viral blog posts across {len(category_map)} categories')
    return count
