from django.db import migrations

def filter_blog_posts_migration(apps, schema_editor):
    BlogPost = apps.get_model('core', 'BlogPost')
    Author = apps.get_model('core', 'Author')

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

    keep_slugs = [
        'django-best-framework-enterprise-web-2026',
        'ui-ux-design-principles-convert-visitors-customers',
        'choose-right-tech-stack-startup-morocco',
    ]

    for post in BlogPost.objects.all():
        if not post.author:
            post.author = author

        if post.slug in keep_slugs:
            post.noindex = False
            post.index_in_sitemap = True
        else:
            post.noindex = True
            post.index_in_sitemap = False
        post.save()

def reverse_filter_blog_posts(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_expand_city_service_content'),
    ]

    operations = [
        migrations.RunPython(filter_blog_posts_migration, reverse_filter_blog_posts),
    ]
