from django.db import migrations


def update_siteconfig_metadata(apps, schema_editor):
    SiteConfig = apps.get_model('core', 'SiteConfig')
    cfg = SiteConfig.objects.first()
    if cfg:
        cfg.blog_seo_title_en = 'Tech & Engineering Blog | getNexiro'
        cfg.blog_seo_title_fr = 'Blog Tech & Ingénierie | getNexiro'
        cfg.blog_seo_title_ar = 'مدونة التكنولوجيا والهندسة | getNexiro'
        cfg.hero_subtitle_fr = "Agence web à Tanger spécialisée dans la création de site web et le développement d'applications mobiles au Maroc. Nous concevons des systèmes numériques haute performance pour entreprises et partenaires nearshore."
        cfg.hero_subtitle_ar = "وكالة تطوير مواقع وتطبيقات بطنجة متخصصة في تصميم وتطوير المواقع وتطبيقات الجوال في المغرب، مع حلول هندسية عالية الأداء للشركات المحلية والدولية."
        cfg.save()


def reverse_siteconfig_metadata(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_city_short_slugs_and_landmarks'),
    ]

    operations = [
        migrations.RunPython(update_siteconfig_metadata, reverse_siteconfig_metadata),
    ]
