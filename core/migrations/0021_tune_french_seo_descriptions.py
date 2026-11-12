from django.db import migrations

def tune_french_descriptions(apps, schema_editor):
    SiteConfig = apps.get_model('core', 'SiteConfig')
    cfg = SiteConfig.objects.first()
    if cfg:
        cfg.home_seo_description_fr = "Agence web et mobile à Tanger au Maroc. Nous concevons des applications performantes pour entreprises. Demandez votre devis gratuit dès aujourd'hui."
        cfg.about_seo_description_fr = "Découvrez getNexiro, agence web et mobile à Tanger au Maroc. Explorez notre équipe, nos valeurs et nos méthodes. Contactez-nous pour votre projet."
        cfg.services_seo_description_fr = "Développement web sur mesure, apps mobiles, design UI/UX et cloud à Tanger au Maroc. Solutions scalables. Demandez une consultation gratuite."
        cfg.blog_seo_description_fr = "Guides Django, architecture web, design UI/UX et analyses tech au Maroc. Lisez nos analyses d'ingénierie logicielle et accélérez vos projets."
        cfg.packages_seo_description_fr = "Packs de développement au forfait pour sites web et applications mobiles au Maroc. Tarifs transparents et engagement clair. Découvrez nos offres."
        cfg.save()

def reverse_tune(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0020_filter_and_attribute_blog_posts'),
    ]

    operations = [
        migrations.RunPython(tune_french_descriptions, reverse_tune),
    ]
