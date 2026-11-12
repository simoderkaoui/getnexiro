from django.db import migrations

def update_metrics(apps, schema_editor):
    Project = apps.get_model('core', 'Project')

    # 1. medicenters-performance
    try:
        p = Project.objects.get(slug='medicenters-performance')
        p.results_en = "Significant surge in patient consultation inquiries following launch; higher engagement and session depth driven by interactive 360° clinic tours; exceptional Google PageSpeed loading speeds. [TODO(owner): Provide verified Google Analytics conversion metrics]."
        p.results_fr = "Forte hausse des demandes de consultation médicale après le lancement ; engagement et temps de visite accrus grâce aux visites virtuelles 360° ; score de performance Google PageSpeed optimal. [TODO(owner): Fournir les métriques de conversion vérifiées]."
        p.results_ar = "نمو ملموس في طلبات الاستشارة الطبية بعد الإطلاق؛ وزيادة تفاعل الزوار وعمق الجلسات بفضل الجولات الافتراضية 360 درجة؛ وسرعة تحميل فائقة على مقاييس PageSpeed. [TODO(owner-review): إرفاق أرقام التحليلات الموثقة]."
        p.save()
    except Project.DoesNotExist:
        pass

    # 2. laboratoire-international-tanger
    try:
        p = Project.objects.get(slug='laboratoire-international-tanger')
        p.results_en = "Streamlined patient intake workflow reducing receptionist phone bottlenecks; active recurring monthly online appointment bookings; top local search visibility in Tangier for clinical biology services. [TODO(owner): Confirm exact monthly appointment volumes]."
        p.results_fr = "Optimisation de l'accueil et réduction de l'encombrement téléphonique ; prise de rendez-vous en ligne fluide ; visibilité de premier plan sur les recherches de biologie médicale à Tanger. [TODO(owner): Confirmer les volumes de rendez-vous mensuels]."
        p.results_ar = "تنظيم استقبال المرضى وتخفيف الضغط على الهاتف؛ حجز مواعيد إلكتروني سلس؛ وظهور متقدم في نتائج البحث المحلي بطنجة للتحاليل الطبية. [TODO(owner-review): تأكيد إحصائيات المواعيد الشهرية]."
        p.save()
    except Project.DoesNotExist:
        pass

    # 3. storetanger
    try:
        p = Project.objects.get(slug='storetanger')
        p.results_en = "Strong local search positioning in Northern Morocco for custom blinds; high direct inquiry conversion via WhatsApp integration; rapid page loads and increased monthly customer consultations. [TODO(owner): Confirm exact rank and inquiry growth multiplier]."
        p.results_fr = "Positionnement de premier plan dans le Nord du Maroc pour les stores et rideaux ; forte conversion des demandes via l'intégration WhatsApp ; temps de chargement rapides et hausse des demandes clients. [TODO(owner): Confirmer les classements et le multiplicateur de croissance]."
        p.results_ar = "تصدر نتائج البحث المحلي في شمال المغرب للستائر والمفروشات؛ وتدفق مستمر للاستفسارات المباشرة عبر واتساب؛ وسرعة تصفح عالية. [TODO(owner-review): تأكيد الأرقام ومعدل النمو]."
        p.save()
    except Project.DoesNotExist:
        pass

    # 4. ecran-led-tanger
    try:
        p = Project.objects.get(slug='ecran-led-tanger')
        p.results_en = "Prominent Google visibility in Tangier for commercial LED displays and event rentals; consistent growth in qualified B2B quote inquiries during the post-launch phase. [TODO(owner): Confirm B2B quote percentage increase]."
        p.results_fr = "Visibilité Google de premier plan à Tanger pour les écrans LED et la location événementielle ; croissance soutenue des demandes de devis B2B qualifiées. [TODO(owner): Confirmer le pourcentage de hausse des devis]."
        p.results_ar = "ظهور بارز على نتائج بحث جوجل بطنجة لشاشات العرض والتأجير؛ ونمو مستمر في طلبات عروض الأسعار الموجهة للشركات. [TODO(owner-review): تأكيد نسبة نمو عروض الأسعار]."
        p.save()
    except Project.DoesNotExist:
        pass

def reverse_metrics(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0021_tune_french_seo_descriptions'),
    ]

    operations = [
        migrations.RunPython(update_metrics, reverse_metrics),
    ]
