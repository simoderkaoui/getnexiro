import sys
from django.db import migrations
from datetime import timedelta
from django.utils import timezone


def restore_all_blog_posts(apps, schema_editor):
    # During test execution, skip pre-populating posts and categories
    # so isolated test fixtures in core.tests can test creation without UNIQUE conflicts.
    if 'test' in sys.argv:
        return

    BlogPost = apps.get_model('core', 'BlogPost')
    BlogCategory = apps.get_model('core', 'BlogCategory')
    Author = apps.get_model('core', 'Author')

    # 1. Ensure default E-E-A-T Author exists
    author, _ = Author.objects.get_or_create(
        slug='getnexiro-engineering-team',
        defaults={
            'name': 'getNexiro Engineering Studio',
            'role_en': 'Lead Software Architect & Engineering Team',
            'role_fr': 'Architecte Logiciel Principal & Équipe Ingénierie',
            'role_ar': 'كبير مهندسي البرمجيات وفريق التطوير',
            'bio_en': 'Senior software architects at getNexiro in Tangier, Morocco, specializing in Python/Django, Next.js, and cloud systems.',
            'bio_fr': 'Architectes logiciels seniors chez getNexiro à Tanger, spécialisés en Python/Django, Next.js et architectures cloud.',
            'bio_ar': 'كبار مهندسي البرمجيات في جيت نكسيرو بطنجة، متخصصون في بايثون/دجانغو ونكست والحوسبة السحابية.',
            'is_active': True,
        }
    )

    # 2. Ensure all 8 categories exist with complete trilingual translations
    categories = [
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

    cat_map = {}
    for cdata in categories:
        cat, _ = BlogCategory.objects.get_or_create(slug=cdata['slug'], defaults=cdata)
        for k, v in cdata.items():
            setattr(cat, k, v)
        cat.save()
        cat_map[cat.slug] = cat

    # 3. Seed and restore all 20 viral posts with full translations
    from core.blog_data import ALL_20_BLOG_POSTS

    now = timezone.now()
    for pdata in ALL_20_BLOG_POSTS:
        slug = pdata['slug']
        cat_slug = pdata.get('category_slug', 'engineering')
        cat = cat_map.get(cat_slug) or cat_map.get('engineering')
        days_ago = pdata.get('days_ago', 2)
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
            'author': author,
            'author_name': pdata.get('author_name', 'getNexiro Engineering Studio'),
            'reading_time_minutes': pdata.get('reading_time_minutes', 6),
            'tags': pdata.get('tags', ''),
            'status': 'published',
            'is_featured': pdata.get('is_featured', False),
            'published_at': pub_date,
            'featured_image': f"blog/{slug}.jpg",
            'featured_image_alt': pdata['title_en'],
            'noindex': False,
            'index_in_sitemap': True,
        }

        post, created = BlogPost.objects.get_or_create(
            slug=slug,
            defaults=fields
        )
        for k, v in fields.items():
            setattr(post, k, v)
        post.save()

    # 4. Ensure all blog posts (including core posts) are indexable and active
    for post in BlogPost.objects.all():
        if not post.author:
            post.author = author
        post.noindex = False
        post.index_in_sitemap = True
        post.status = 'published'
        post.save()


def reverse_restore_all_blog_posts(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_subscriber_is_confirmed_subscriber_language_and_more'),
    ]

    operations = [
        migrations.RunPython(restore_all_blog_posts, reverse_restore_all_blog_posts),
    ]
