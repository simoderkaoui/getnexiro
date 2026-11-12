from django.db import migrations

def clear_github(apps, schema_editor):
    SiteConfig = apps.get_model('core', 'SiteConfig')
    cfg = SiteConfig.objects.first()
    if cfg and 'simoderkaoui' in (cfg.github_url or ''):
        cfg.github_url = ''
        cfg.save()

def reverse_github(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0022_rephrase_unverified_project_metrics'),
    ]

    operations = [
        migrations.RunPython(clear_github, reverse_github),
    ]
