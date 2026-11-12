from django.db import migrations

def update_hero_and_stats(apps, schema_editor):
    SiteConfig = apps.get_model('core', 'SiteConfig')
    Stat = apps.get_model('core', 'Stat')

    config = SiteConfig.objects.first()
    if config:
        config.hero_title_en = "Web & App Development Agency in Tangier, Morocco"
        config.hero_title_fr = "Agence de développement web et mobile à Tanger"
        config.hero_title_ar = "وكالة تطوير مواقع وتطبيقات بطنجة"

        config.hero_subtitle_en = "We architect high-velocity digital systems. Bespoke web platforms, mobile applications, and resilient cloud software for growing businesses in Tangier, Morocco, and European companies seeking nearshore engineering excellence."
        config.hero_subtitle_fr = "Nous concevons des systèmes numériques haute performance. Applications web et mobiles sur mesure pour les entreprises à Tanger, au Maroc et les sociétés européennes en quête d'excellence nearshore."
        config.hero_subtitle_ar = "نبتكر حلولاً برمجية وأنظمة رقمية متطورة. منصات ويب وتطبيقات هواتف مخصصة للشركات في طنجة والمغرب، وخدمات هندسية رائدة لشركائنا في أوروبا."
        config.save()

    # Update stats to truthful, verified metrics
    Stat.objects.all().delete()
    stats_data = [
        ('10+', 'Production Case Studies', 'Études de Cas en Production', 'أكثر من 10 دراسات حالة وأنظمة حية', 1),
        ('5', 'Core Engineering Disciplines', 'Disciplines d\'Ingénierie Clés', '5 تخصصات هندسية رئيسية', 2),
        ('3', 'Supported Languages (EN/FR/AR)', 'Langues Prises en Charge (EN/FR/AR)', '3 لغات معتمدة (العربية/الفرنسية/الإنجليزية)', 3),
        ('GMT+1', 'Tangier Hub / European Timezone', 'Hub de Tanger / Fuseau Européen', 'مركز طنجة / توقيت متزامن مع أوروبا', 4),
    ]
    for val, en, fr, ar, order in stats_data:
        Stat.objects.create(value=val, label_en=en, label_fr=fr, label_ar=ar, order=order)

def reverse_hero_and_stats(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_populate_seo_metadata'),
    ]

    operations = [
        migrations.RunPython(update_hero_and_stats, reverse_hero_and_stats),
    ]
