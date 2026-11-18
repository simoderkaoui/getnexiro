# Generated manually for full Local City SEO optimization

from django.db import migrations


def optimize_cities_seo(apps, schema_editor):
    CityServicePage = apps.get_model('core', 'CityServicePage')

    city_names = {
        'tangier': {'en': 'Tangier', 'fr': 'Tanger', 'ar': 'طنجة'},
        'tetouan': {'en': 'Tetouan', 'fr': 'Tétouan', 'ar': 'تطوان'},
        'fes': {'en': 'Fes', 'fr': 'Fès', 'ar': 'فاس'},
        'meknes': {'en': 'Meknes', 'fr': 'Meknès', 'ar': 'مكناس'},
        'mdiq': {'en': "M'diq", 'fr': "M'diq", 'ar': 'المضيق'},
        'chefchaouen': {'en': 'Chefchaouen', 'fr': 'Chefchaouen', 'ar': 'شفشاون'},
        'larache': {'en': 'Larache', 'fr': 'Larache', 'ar': 'العرائش'},
        'kenitra': {'en': 'Kenitra', 'fr': 'Kénitra', 'ar': 'القنيطرة'},
    }

    service_titles = {
        'web-development': {
            'en': 'Web Development',
            'fr': 'Développement Web',
            'ar': 'تطوير مواقع وتطبيقات الويب',
        },
        'mobile-applications': {
            'en': 'Mobile App Development',
            'fr': 'Développement Mobile',
            'ar': 'تطوير تطبيقات الجوال',
        },
        'uiux-design-systems': {
            'en': 'UI/UX Design Studio',
            'fr': 'Design UI/UX & Systèmes',
            'ar': 'تصميم واجهات وتجربة المستخدم',
        },
    }

    for page in CityServicePage.objects.all():
        city_code = page.city
        c_names = city_names.get(city_code, {'en': city_code.capitalize(), 'fr': city_code.capitalize(), 'ar': city_code})
        svc_slug = page.service.slug if page.service else 'web-development'
        s_names = service_titles.get(svc_slug, {
            'en': page.service.title_en if page.service else 'Software Development',
            'fr': page.service.title_fr if page.service and page.service.title_fr else 'Développement Logiciel',
            'ar': page.service.title_ar if page.service and page.service.title_ar else 'تطوير البرمجيات',
        })

        # All cities are published and indexable by search engines
        page.is_published = True
        page.noindex = False

        # SEO Titles (< 60 chars)
        page.seo_title_en = f"{s_names['en']} in {c_names['en']} | getNexiro"
        page.seo_title_fr = f"{s_names['fr']} à {c_names['fr']} | getNexiro"
        page.seo_title_ar = f"{s_names['ar']} في {c_names['ar']} | getNexiro"

        # SEO Descriptions (120 - 155 chars)
        page.seo_description_en = (
            f"Expert {s_names['en'].lower()} services for companies in {c_names['en']}, Morocco. "
            f"Custom software platforms & mobile apps by getNexiro. Request your free quote."
        )
        if len(page.seo_description_en) > 155:
            page.seo_description_en = page.seo_description_en[:154] + '.'

        page.seo_description_fr = (
            f"Services experts en {s_names['fr'].lower()} pour entreprises à {c_names['fr']}, Maroc. "
            f"Applications web et mobiles sur mesure par getNexiro. Devis gratuit sous 24h."
        )
        if len(page.seo_description_fr) > 155:
            page.seo_description_fr = page.seo_description_fr[:154] + '.'

        page.seo_description_ar = (
            f"خدمات احترافية في {s_names['ar']} للشركات والمؤسسات في {c_names['ar']} بالمغرب. "
            f"أنظمة برمجية وتطبيقات مخصصة من getNexiro. اطلب عرض سعر مجاني اليوم."
        )
        if len(page.seo_description_ar) > 155:
            page.seo_description_ar = page.seo_description_ar[:154] + '.'

        # Landmarks check
        if city_code == 'tangier':
            if not page.local_landmarks_en:
                page.local_landmarks_en = "Tanger Med Port & Logistics Zone\nTangier Free Zone (TFZ) & Automotive City (TAC)\nIbn Batouta Business Hub & City Center"
                page.local_landmarks_fr = "Port Tanger Med & Zone Logistique\nTangier Free Zone (TFZ) & Tanger Automotive City (TAC)\nCentre d'Affaires Ibn Batouta"
                page.local_landmarks_ar = "ميناء طنجة المتوسط والمنطقة اللوجستية\nمنطقة طنجة الحرة (TFZ) ومدينة صناعة السيارات (TAC)\nمركز ابن بطوطة للأعمال ووسط المدينة"
        elif city_code == 'tetouan':
            if not page.local_landmarks_en:
                page.local_landmarks_en = "Tetouan Shore Nearshoring Park\nTamuda Bay Commercial Hub\nTétouan Industrial Park"
                page.local_landmarks_fr = "Parc Offshoring Tetouan Shore\nPôle Économique Tamuda Bay\nZone Industrielle de Tétouan"
                page.local_landmarks_ar = "منتزه تطوان شور للخدمات المرحلية\nالقطب التجاري تامودا باي\nالمنطقة الصناعية بتطوان"
        elif city_code == 'fes':
            if not page.local_landmarks_en:
                page.local_landmarks_en = "Fes Shore Offshore Park\nSidi Brahim Industrial Zone\nRoute de Sefrou Business District"
                page.local_landmarks_fr = "Parc Offshore Fes Shore\nZone Industrielle Sidi Brahim\nQuartier d'Affaires Route de Sefrou"
                page.local_landmarks_ar = "منتزه فاس شور للأوفشورينغ\nالمنطقة الصناعية سيدي براهيم\nحي الأعمال طريق صفرو"
        elif city_code == 'meknes':
            if not page.local_landmarks_en:
                page.local_landmarks_en = "Agropolis Meknes Food Cluster\nSidi Bouzekri Industrial Zone\nMejjat Commercial District"
                page.local_landmarks_fr = "Agropolis Meknès Agropole\nZone Industrielle Sidi Bouzekri\nZone Commerciale Mejjat"
                page.local_landmarks_ar = "القطب الفلاحي أكروبوليس مكناس\nالمنطقة الصناعية سيدي بوزكري\nالمنطقة التجارية مجاط"

        page.save()


def reverse_optimize(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_project_description_en'),
    ]

    operations = [
        migrations.RunPython(optimize_cities_seo, reverse_optimize),
    ]
