"""
Seed the database with complete multilingual content (English, French, Arabic).
Robust against network failures and proxy blocks (checks local media files first).

Usage: python manage.py seed_data
"""

import os
import urllib.request
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from core.models import (
    SiteConfig, Service, ServiceSolution, ProjectCategory, Project, ProjectImage,
    TeamMember, Testimonial, ClientLogo, Stat,
    CompanyValue, ProcessStep, StoreItem, BlogCategory, BlogPost,
)


def get_image_file(subfolder, seed, filename, download_url):
    """
    Get image from local media first (offline-friendly for PythonAnywhere),
    then try downloading, with graceful fallback.
    """
    media_dir = Path(settings.MEDIA_ROOT) / subfolder
    target_file = media_dir / filename

    # 1. Exact local file exists
    if target_file.exists() and target_file.stat().st_size > 0:
        try:
            with open(target_file, 'rb') as f:
                return ContentFile(f.read(), name=filename)
        except Exception:
            pass

    # 2. Match any file starting with seed in that folder
    if media_dir.exists():
        for candidate in media_dir.glob(f'{seed}*'):
            if candidate.is_file() and candidate.stat().st_size > 0:
                try:
                    with open(candidate, 'rb') as f:
                        return ContentFile(f.read(), name=candidate.name)
                except Exception:
                    pass

    # 3. Try to download from internet (works locally or on paid tiers)
    try:
        req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=8).read()
        if data:
            # Save locally for future runs
            media_dir.mkdir(parents=True, exist_ok=True)
            try:
                with open(target_file, 'wb') as f:
                    f.write(data)
            except Exception:
                pass
            return ContentFile(data, name=filename)
    except Exception as e:
        print(f'  [NOTE] Offline mode: could not fetch {download_url} ({e})')

    # 4. Fallback to logo in static
    static_logo = Path(settings.BASE_DIR) / 'static' / 'images' / 'logo.png'
    if static_logo.exists():
        try:
            with open(static_logo, 'rb') as f:
                return ContentFile(f.read(), name=f'{seed}.png')
        except Exception:
            pass

    return None


class Command(BaseCommand):
    help = 'Seeds database with complete multilingual content for getNexiro.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding getNexiro multilingual database...')

        # ── 1. SiteConfig ──
        config = SiteConfig.load()
        config.site_name = 'getNexiro'
        config.email = 'getnexiro@gmail.com'
        config.phone = '+212 787 862 187'
        config.hero_bg_type = 'video'

        config.tagline_en = 'Tech & Dev Services'
        config.tagline_fr = 'Services Tech & Dev'
        config.tagline_ar = 'خدمات التكنولوجيا والتطوير'

        config.hero_title_en = 'We Architect High-Velocity Digital Systems'
        config.hero_title_fr = 'Nous Concevons des Systèmes Numériques Haute-Performance'
        config.hero_title_ar = 'نصمم أنظمة رقمية عالية السرعة والأداء'

        config.hero_badge_en = 'B2B Software Studio • Tangier, Morocco'
        config.hero_badge_fr = 'Studio Logiciel B2B • Tanger, Maroc'
        config.hero_badge_ar = 'استوديو برمجيات B2B • طنجة، المغرب'

        config.hero_cta_primary_text_en = 'Start a Project'
        config.hero_cta_primary_text_fr = 'Démarrer un projet'
        config.hero_cta_primary_text_ar = 'ابدأ مشروعك'

        config.hero_cta_secondary_text_en = 'Selected Work'
        config.hero_cta_secondary_text_fr = 'Nos Réalisations'
        config.hero_cta_secondary_text_ar = 'أعمال مختارة'

        config.cta_title_en = 'Ready to Elevate Your Digital Presence?'
        config.cta_title_fr = 'Prêt à propulser votre présence numérique ?'
        config.cta_title_ar = 'هل أنت مستعد لتعزيز حضورك الرقمي؟'

        config.cta_subtitle_en = "Let's discuss your next project and explore how getNexiro can help you achieve your business goals."
        config.cta_subtitle_fr = "Parlons de votre prochain projet et voyons comment getNexiro peut propulser vos objectifs d'affaires."
        config.cta_subtitle_ar = "دعنا نناقش مشروعك القادم ونكتشف معاً كيف تساعدك getNexiro على تحقيق أهدافك التجارية بنجاح."

        config.cta_button_text_en = 'Start a Project'
        config.cta_button_text_fr = 'Démarrer un projet'
        config.cta_button_text_ar = 'ابدأ مشروعك معنا'

        config.hero_subtitle_en = (
            'A premium software engineering agency crafting scalable web platforms, '
            'bespoke enterprise applications, and resilient digital architectures for '
            'forward-thinking organizations worldwide.'
        )
        config.hero_subtitle_fr = (
            'Une agence d\'ingénierie logicielle haut de gamme concevant des plateformes web '
            'évolutives, des applications d\'entreprise sur mesure et des architectures numériques '
            'résilientes pour les organisations visionnaires.'
        )
        config.hero_subtitle_ar = (
            'وكالة رائدة في هندسة البرمجيات تصمم منصات ويب قابلة للتوسع وتطبيقات مؤسسية '
            'مخصصة وبنيات تحتية رقمية مرنة للمؤسسات الطموحة في طنجة والمغرب والعالم.'
        )

        config.about_text_en = (
            "Founded in Tangier — the vibrant city where the Atlantic meets the Mediterranean — "
            "getNexiro was born from a simple belief: world-class software doesn't need a Silicon Valley address."
        )
        config.about_text_fr = (
            "Fondée à Tanger — la ville vibrante où l'Atlantique rencontre la Méditerranée — "
            "getNexiro est née d'une conviction simple : les logiciels de classe mondiale n'ont pas besoin d'une adresse dans la Silicon Valley."
        )
        config.about_text_ar = (
            "تأسست getNexiro في طنجة — المدينة النابضة بالحياة حيث يلتقي الأطلسي بالمتوسط — "
            "من إيمان راسخ: البرمجيات العالمية لا تحتاج إلى عنوان في وادي السيليكون لتتفوق."
        )

        config.mission_statement_en = (
            'To empower enterprises with bespoke digital solutions that are not just functional, '
            'but transformative — combining technical excellence with strategic insight.'
        )
        config.mission_statement_fr = (
            'Donner aux entreprises les moyens d\'agir grâce à des solutions numériques sur mesure '
            'qui ne sont pas seulement fonctionnelles, mais transformatrices — alliant excellence technique et vision stratégique.'
        )
        config.mission_statement_ar = (
            'تمكين الشركات والمؤسسات من خلال حلول رقمية مخصصة ليست فقط وظيفية، بل تحويلية — '
            'تجمع بين التميز الهندسي والرؤية الاستراتيجية لتحقيق ميزة تنافسية مستدامة.'
        )

        config.address_en = 'Tangier 90000, Morocco'
        config.address_fr = 'Tanger 90000, Maroc'
        config.address_ar = 'طنجة 90000، المغرب'

        config.address_detail_en = 'Ibn Batouta Bureaux, Av. Youssef Ibn Tachfine'
        config.address_detail_fr = 'Bureaux Ibn Batouta, Av. Youssef Ibn Tachfine'
        config.address_detail_ar = 'مكاتب ابن بطوطة، شارع يوسف بن تاشفين'

        config.business_hours_en = 'Mon — Fri: 9:00 AM — 6:00 PM (GMT+1)'
        config.business_hours_fr = 'Lun — Ven : 9h00 — 18h00 (GMT+1)'
        config.business_hours_ar = 'الإثنين — الجمعة: 9:00 ص — 6:00 م (GMT+1)'

        config.meta_description_en = 'getNexiro — Professional web development, mobile apps & software engineering agency in Tangier, Morocco.'
        config.meta_description_fr = 'getNexiro — Agence de développement web, applications mobiles et ingénierie logicielle à Tanger, Maroc.'
        config.meta_description_ar = 'getNexiro — وكالة رائدة في تطوير المواقع وتطبيقات الجوال وهندسة البرمجيات في طنجة، المغرب.'

        config.save()
        self.stdout.write('  [OK] SiteConfig updated with EN / FR / AR')

        # ── 2. Statistics ──
        Stat.objects.all().delete()
        stats_data = [
            ('99.98%', 'System Reliability SLA', 'SLA de Fiabilité Système', 'اتفاقية مستوى موثوقية 99.98%', 1),
            ('50+', 'Enterprise Platforms Shipped', 'Plateformes d\'Entreprise Livrées', 'أكثر من 50 منصة مؤسسية مكتملة', 2),
            ('<80ms', 'Average API Response Latency', 'Temps de Réponse API Moyen', 'متوسط زمن استجابة واجهة API أقل من 80ms', 3),
            ('GMT+1', 'Tangier Hub / European Timezone', 'Hub de Tanger / Fuseau Européen', 'مركز طنجة / توقيت متزامن مع أوروبا', 4),
        ]
        for val, en, fr, ar, order in stats_data:
            Stat.objects.create(value=val, label_en=en, label_fr=fr, label_ar=ar, order=order)
        self.stdout.write(f'  [OK] Created {len(stats_data)} multilingual stats')

        # ── 3. Services ──
        Service.objects.all().delete()
        ServiceSolution.objects.all().delete()
        services_data = [
            {
                'title_en': 'Web Development',
                'title_fr': 'Développement Web',
                'title_ar': 'تطوير مواقع وتطبيقات الويب',
                'subtitle_en': 'Scalable web platforms engineered for growth',
                'subtitle_fr': 'Plateformes web scalables conçues pour la croissance',
                'subtitle_ar': 'منصات ويب قابلة للتوسع مصممة للنمو',
                'description_en': 'From responsive marketing sites to complex SaaS platforms, we architect and build robust web solutions using Django, React, and modern cloud stacks.',
                'description_fr': 'Des sites vitrines réactifs aux plateformes SaaS complexes, nous concevons et bâtissons des solutions web robustes avec Django, React et les stacks cloud modernes.',
                'description_ar': 'من المواقع التعريفية التفاعلية إلى منصات SaaS السحابية المعقدة، نصمم ونطور حلول ويب فائقة الأداء باستخدام Django و React وأحدث التقنيات.',
                'methodology_en': 'We follow an agile methodology with 2-week sprints, continuous integration via GitHub Actions, and automated testing at every stage. Our architecture-first approach ensures your application scales seamlessly from MVP to enterprise.',
                'methodology_fr': 'Nous suivons une méthodologie agile avec des sprints de 2 semaines, intégration continue via GitHub Actions et tests automatisés à chaque étape.',
                'methodology_ar': 'نتبع منهجية أجايل بدورات تطوير كل أسبوعين، تكامل مستمر عبر GitHub Actions، واختبارات آلية في كل مرحلة.',
                'deliverables_en': 'Responsive website or web application\nAdmin dashboard & CMS\nAPI documentation\nPerformance optimization report\nSEO audit & implementation\nDeployment & hosting setup',
                'deliverables_fr': 'Site web ou application web responsive\nTableau de bord admin & CMS\nDocumentation API\nRapport d\'optimisation des performances\nAudit SEO & implémentation\nDéploiement & configuration hébergement',
                'deliverables_ar': 'موقع أو تطبيق ويب متجاوب\nلوحة إدارة ونظام إدارة محتوى\nتوثيق API\nتقرير تحسين الأداء\nتدقيق SEO والتنفيذ\nالنشر وإعداد الاستضافة',
                'technologies': 'Django, React, Next.js, PostgreSQL, Redis, Docker, AWS, Tailwind CSS',
                'timeline': '4 — 12 Weeks',
                'icon': 'icon-web', 'is_featured': True, 'order': 1,
                'solutions': [
                    {'title_en': 'Corporate Websites', 'title_fr': 'Sites Corporatifs', 'title_ar': 'مواقع الشركات', 'description_en': 'Professional brand-forward websites with CMS, multilingual support, and conversion-optimized landing pages.', 'description_fr': 'Sites professionnels avec CMS, support multilingue et pages d\'atterrissage optimisées.', 'description_ar': 'مواقع احترافية مع نظام إدارة محتوى ودعم متعدد اللغات وصفحات هبوط محسنة.', 'icon_emoji': '🌐', 'order': 1},
                    {'title_en': 'SaaS Platforms', 'title_fr': 'Plateformes SaaS', 'title_ar': 'منصات SaaS', 'description_en': 'Multi-tenant SaaS applications with subscription billing, user management, and analytics dashboards.', 'description_fr': 'Applications SaaS multi-locataires avec facturation par abonnement et tableaux de bord analytiques.', 'description_ar': 'تطبيقات SaaS متعددة المستأجرين مع فوترة اشتراك ولوحات تحليلية.', 'icon_emoji': '🚀', 'order': 2},
                    {'title_en': 'E-Commerce Solutions', 'title_fr': 'Solutions E-Commerce', 'title_ar': 'حلول التجارة الإلكترونية', 'description_en': 'Full-featured online stores with payment gateways, inventory management, and order tracking systems.', 'description_fr': 'Boutiques en ligne complètes avec passerelles de paiement et gestion des stocks.', 'description_ar': 'متاجر إلكترونية متكاملة مع بوابات دفع وإدارة مخزون.', 'icon_emoji': '🛒', 'order': 3},
                ],
            },
            {
                'title_en': 'Mobile Applications',
                'title_fr': 'Applications Mobiles',
                'title_ar': 'تطوير تطبيقات الجوال',
                'subtitle_en': 'Native & cross-platform apps that users love',
                'subtitle_fr': 'Applications natives et multiplateformes que les utilisateurs adorent',
                'subtitle_ar': 'تطبيقات أصلية ومتعددة المنصات يحبها المستخدمون',
                'description_en': 'Native iOS/Android and cross-platform apps built with Flutter and React Native, delivering seamless performance and intuitive user interfaces.',
                'description_fr': 'Applications natives iOS/Android et multiplateformes avec Flutter et React Native, offrant une fluidité parfaite et une ergonomie intuitive.',
                'description_ar': 'تطبيقات أصلية لنظامي iOS و Android وتطبيقات هجينة عبر Flutter و React Native، بأداء سلس وتصميم واجهات مستخدم جذاب.',
                'methodology_en': 'Component-driven development with atomic design principles. We prototype in Figma, build reusable widget libraries, and ship with automated CI/CD pipelines for both App Store and Google Play.',
                'methodology_fr': 'Développement orienté composants avec principes de design atomique. Prototypage Figma et déploiement CI/CD automatisé.',
                'methodology_ar': 'تطوير قائم على المكونات مع مبادئ التصميم الذري. نماذج أولية في Figma ونشر CI/CD آلي.',
                'deliverables_en': 'iOS & Android applications\nUI/UX design files (Figma)\nBackend API integration\nPush notification system\nApp Store & Play Store submission\nPost-launch analytics setup',
                'deliverables_fr': 'Applications iOS & Android\nFichiers design UI/UX (Figma)\nIntégration API backend\nSystème de notifications push\nSoumission App Store & Play Store\nConfiguration analytics post-lancement',
                'deliverables_ar': 'تطبيقات iOS و Android\nملفات تصميم UI/UX (Figma)\nتكامل API الخلفية\nنظام إشعارات فورية\nنشر على App Store و Play Store\nإعداد التحليلات بعد الإطلاق',
                'technologies': 'Flutter, React Native, Swift, Kotlin, Firebase, Supabase',
                'timeline': '6 — 14 Weeks',
                'icon': 'icon-mobile', 'is_featured': True, 'order': 2,
                'solutions': [
                    {'title_en': 'Consumer Apps', 'title_fr': 'Apps Grand Public', 'title_ar': 'تطبيقات المستهلكين', 'description_en': 'Engaging consumer-facing applications with social features, gamification, and real-time updates.', 'description_fr': 'Applications engageantes avec fonctionnalités sociales, gamification et mises à jour en temps réel.', 'description_ar': 'تطبيقات جذابة مع ميزات اجتماعية وألعاب وتحديثات فورية.', 'icon_emoji': '📱', 'order': 1},
                    {'title_en': 'Enterprise Mobile', 'title_fr': 'Mobile Entreprise', 'title_ar': 'تطبيقات المؤسسات', 'description_en': 'Internal enterprise apps for field operations, inventory scanning, and workforce management.', 'description_fr': 'Apps internes pour opérations terrain, scan d\'inventaire et gestion du personnel.', 'description_ar': 'تطبيقات داخلية لعمليات الميدان ومسح المخزون وإدارة القوى العاملة.', 'icon_emoji': '🏢', 'order': 2},
                    {'title_en': 'IoT Companion Apps', 'title_fr': 'Apps IoT Compagnon', 'title_ar': 'تطبيقات إنترنت الأشياء', 'description_en': 'Mobile apps that interface with IoT devices, sensors, and hardware via Bluetooth or Wi-Fi.', 'description_fr': 'Apps mobiles interfaçant avec appareils IoT, capteurs et hardware via Bluetooth ou Wi-Fi.', 'description_ar': 'تطبيقات جوال تتواصل مع أجهزة إنترنت الأشياء والمستشعرات عبر البلوتوث أو الواي فاي.', 'icon_emoji': '📡', 'order': 3},
                ],
            },
            {
                'title_en': 'UI/UX & Design Systems',
                'title_fr': 'UI/UX & Design Systems',
                'title_ar': 'تصميم تجربة وواجهة المستخدم',
                'subtitle_en': 'Human-centered design that drives engagement',
                'subtitle_fr': 'Design centré sur l\'humain qui stimule l\'engagement',
                'subtitle_ar': 'تصميم محوره الإنسان يعزز التفاعل',
                'description_en': 'User research, wireframing, interactive prototyping, and pixel-perfect design systems that elevate your brand and maximize conversion.',
                'description_fr': 'Recherche utilisateur, prototypage interactif et design systems au pixel près pour sublimer votre marque et maximiser vos conversions.',
                'description_ar': 'أبحاث تجربة المستخدم، النماذج التفاعلية، وتصميم أنظمة واجهات متكاملة ترتقي بعلامتك التجارية وتضاعف معدلات التحويل.',
                'methodology_en': 'Design thinking methodology: Empathize → Define → Ideate → Prototype → Test. We validate every design decision with real user testing and A/B experiments.',
                'methodology_fr': 'Méthodologie Design Thinking : Empathie → Définition → Idéation → Prototype → Test. Validation par tests utilisateurs réels.',
                'methodology_ar': 'منهجية التفكير التصميمي: تعاطف ← تعريف ← توليد أفكار ← نموذج أولي ← اختبار. نتحقق من كل قرار تصميمي بالاختبار مع مستخدمين حقيقيين.',
                'deliverables_en': 'User research report & personas\nWireframes & information architecture\nInteractive Figma prototypes\nDesign system & component library\nBrand style guide\nUsability testing report',
                'deliverables_fr': 'Rapport de recherche utilisateur & personas\nWireframes & architecture de l\'information\nPrototypes interactifs Figma\nDesign system & bibliothèque de composants\nGuide de style de marque\nRapport de tests d\'utilisabilité',
                'deliverables_ar': 'تقرير بحث المستخدم والشخصيات\nالهياكل السلكية وبنية المعلومات\nنماذج Figma التفاعلية\nنظام تصميم ومكتبة مكونات\nدليل هوية العلامة التجارية\nتقرير اختبارات قابلية الاستخدام',
                'technologies': 'Figma, Adobe Creative Suite, Storybook, Tailwind CSS, Framer Motion',
                'timeline': '3 — 8 Weeks',
                'icon': 'icon-design', 'is_featured': True, 'order': 3,
                'solutions': [
                    {'title_en': 'UX Audits & Research', 'title_fr': 'Audits UX & Recherche', 'title_ar': 'تدقيق وأبحاث UX', 'description_en': 'Comprehensive UX audits with heuristic evaluation, user interviews, and analytics-driven recommendations.', 'description_fr': 'Audits UX complets avec évaluation heuristique, entretiens utilisateurs et recommandations basées sur les données.', 'description_ar': 'تدقيق شامل لتجربة المستخدم مع تقييم استكشافي ومقابلات وتوصيات مبنية على البيانات.', 'icon_emoji': '🔍', 'order': 1},
                    {'title_en': 'Design Systems', 'title_fr': 'Design Systems', 'title_ar': 'أنظمة التصميم', 'description_en': 'Reusable component libraries with consistent tokens, patterns, and documentation for scalable product design.', 'description_fr': 'Bibliothèques de composants réutilisables avec tokens, patterns et documentation cohérents.', 'description_ar': 'مكتبات مكونات قابلة لإعادة الاستخدام مع رموز وأنماط وتوثيق متسق.', 'icon_emoji': '🎨', 'order': 2},
                    {'title_en': 'Conversion Optimization', 'title_fr': 'Optimisation des Conversions', 'title_ar': 'تحسين معدلات التحويل', 'description_en': 'Data-driven landing page design and A/B testing strategies to maximize your conversion funnel.', 'description_fr': 'Design de pages d\'atterrissage basé sur les données et stratégies de test A/B.', 'description_ar': 'تصميم صفحات هبوط مبني على البيانات واستراتيجيات اختبار A/B لتعظيم قمع التحويل.', 'icon_emoji': '📈', 'order': 3},
                ],
            },
            {
                'title_en': 'Technical Consulting',
                'title_fr': 'Conseil Technique',
                'title_ar': 'الاستشارات التقنية والمعمارية',
                'subtitle_en': 'Strategic technology guidance for enterprise growth',
                'subtitle_fr': 'Conseils technologiques stratégiques pour la croissance',
                'subtitle_ar': 'إرشادات تقنية استراتيجية لنمو المؤسسات',
                'description_en': 'Architecture reviews, security audits, and strategic technology roadmapping to ensure your digital investments deliver maximum enterprise ROI.',
                'description_fr': 'Audits d\'architecture, revues de sécurité et feuilles de route technologiques stratégiques pour rentabiliser vos investissements digitaux.',
                'description_ar': 'تدقيق معمارية الأنظمة، مراجعات الأمان والحماية، ووضع خطط تقنية استراتيجية تضمن تحقيق أعلى عائد على استثماراتكم الرقمية.',
                'methodology_en': 'We employ TOGAF and C4 architecture frameworks combined with threat modeling (STRIDE) for security. Our consulting engagements follow a structured assessment → recommendation → implementation roadmap.',
                'methodology_fr': 'Nous utilisons les frameworks TOGAF et C4 combinés avec la modélisation de menaces (STRIDE) pour la sécurité.',
                'methodology_ar': 'نستخدم أطر عمل TOGAF و C4 مع نمذجة التهديدات (STRIDE) للأمان.',
                'deliverables_en': 'Architecture assessment report\nSecurity audit & penetration test results\nTechnology roadmap (12-24 months)\nCost optimization analysis\nVendor comparison matrix\nImplementation playbook',
                'deliverables_fr': 'Rapport d\'évaluation d\'architecture\nRésultats d\'audit de sécurité\nFeuille de route technologique (12-24 mois)\nAnalyse d\'optimisation des coûts\nMatrice de comparaison des fournisseurs\nManuel d\'implémentation',
                'deliverables_ar': 'تقرير تقييم المعمارية\nنتائج تدقيق الأمان واختبار الاختراق\nخارطة طريق تقنية (12-24 شهرًا)\nتحليل تحسين التكاليف\nمصفوفة مقارنة الموردين\nدليل التنفيذ',
                'technologies': 'TOGAF, AWS Well-Architected, Terraform, OWASP',
                'timeline': '2 — 6 Weeks',
                'icon': 'icon-consulting', 'is_featured': False, 'order': 4,
                'solutions': [
                    {'title_en': 'Architecture Reviews', 'title_fr': 'Revues d\'Architecture', 'title_ar': 'مراجعات المعمارية', 'description_en': 'In-depth analysis of your system architecture with scalability, reliability, and cost recommendations.', 'description_fr': 'Analyse approfondie de votre architecture avec recommandations de scalabilité et fiabilité.', 'description_ar': 'تحليل عميق لمعمارية نظامكم مع توصيات للقابلية للتوسع والموثوقية.', 'icon_emoji': '🏗️', 'order': 1},
                    {'title_en': 'Security Assessments', 'title_fr': 'Évaluations de Sécurité', 'title_ar': 'تقييمات الأمان', 'description_en': 'Comprehensive security audits including penetration testing, vulnerability scanning, and compliance checks.', 'description_fr': 'Audits de sécurité complets incluant tests d\'intrusion et vérifications de conformité.', 'description_ar': 'تدقيقات أمنية شاملة تشمل اختبار الاختراق ومسح الثغرات وفحوصات الامتثال.', 'icon_emoji': '🛡️', 'order': 2},
                    {'title_en': 'Digital Transformation', 'title_fr': 'Transformation Digitale', 'title_ar': 'التحول الرقمي', 'description_en': 'Strategic roadmaps for modernizing legacy systems and adopting cloud-native architectures.', 'description_fr': 'Feuilles de route stratégiques pour moderniser les systèmes existants et adopter le cloud natif.', 'description_ar': 'خرائط طريق استراتيجية لتحديث الأنظمة القديمة واعتماد معماريات السحابة الأصلية.', 'icon_emoji': '🔄', 'order': 3},
                ],
            },
            {
                'title_en': 'API & Microservices',
                'title_fr': 'API & Microservices',
                'title_ar': 'واجهات البرمجة والخدمات المصغرة',
                'subtitle_en': 'High-performance APIs that power your ecosystem',
                'subtitle_fr': 'APIs haute performance qui alimentent votre écosystème',
                'subtitle_ar': 'واجهات برمجية عالية الأداء تغذي نظامك البيئي',
                'description_en': 'High-throughput RESTful and GraphQL APIs, seamless third-party integrations, and fault-tolerant microservices architecture.',
                'description_fr': 'APIs RESTful et GraphQL haute performance, intégrations tierces fluides et architecture microservices résiliente.',
                'description_ar': 'واجهات برمجية RESTful و GraphQL عالية الأداء، تكاملات برمجية سلسة وبنية خدمات مصغرة ذات اعتمادية وموثوقية فائقة.',
                'methodology_en': 'API-first design with OpenAPI specifications, contract testing, and comprehensive documentation. We build event-driven microservices with message queues for reliability.',
                'methodology_fr': 'Conception API-first avec spécifications OpenAPI, tests de contrat et documentation exhaustive.',
                'methodology_ar': 'تصميم API-first مع مواصفات OpenAPI واختبارات العقود وتوثيق شامل.',
                'deliverables_en': 'RESTful or GraphQL API\nOpenAPI/Swagger documentation\nSDK & client libraries\nRate limiting & authentication\nMonitoring & alerting dashboard\nLoad testing results',
                'deliverables_fr': 'API RESTful ou GraphQL\nDocumentation OpenAPI/Swagger\nSDK & bibliothèques client\nLimitation de débit & authentification\nTableau de bord monitoring & alertes\nRésultats de tests de charge',
                'deliverables_ar': 'واجهة برمجية RESTful أو GraphQL\nتوثيق OpenAPI/Swagger\nSDK ومكتبات العميل\nتحديد المعدل والمصادقة\nلوحة مراقبة وتنبيهات\nنتائج اختبارات التحميل',
                'technologies': 'Django REST Framework, GraphQL, RabbitMQ, Celery, gRPC, Kong',
                'timeline': '4 — 10 Weeks',
                'icon': 'icon-api', 'is_featured': False, 'order': 5,
                'solutions': [
                    {'title_en': 'REST & GraphQL APIs', 'title_fr': 'APIs REST & GraphQL', 'title_ar': 'واجهات REST و GraphQL', 'description_en': 'Production-grade APIs with versioning, pagination, filtering, and comprehensive error handling.', 'description_fr': 'APIs de production avec versioning, pagination, filtrage et gestion d\'erreurs complète.', 'description_ar': 'واجهات برمجية بمستوى الإنتاج مع إصدارات وترقيم صفحات وتصفية ومعالجة أخطاء شاملة.', 'icon_emoji': '⚡', 'order': 1},
                    {'title_en': 'Third-Party Integrations', 'title_fr': 'Intégrations Tierces', 'title_ar': 'تكاملات الطرف الثالث', 'description_en': 'Seamless integration with payment gateways, CRMs, ERPs, and external data providers.', 'description_fr': 'Intégration fluide avec passerelles de paiement, CRM, ERP et fournisseurs de données externes.', 'description_ar': 'تكامل سلس مع بوابات الدفع وأنظمة CRM وERP ومزودي البيانات الخارجيين.', 'icon_emoji': '🔗', 'order': 2},
                    {'title_en': 'Event-Driven Architecture', 'title_fr': 'Architecture Événementielle', 'title_ar': 'معمارية مدفوعة بالأحداث', 'description_en': 'Scalable microservices with message queues, event sourcing, and CQRS patterns.', 'description_fr': 'Microservices scalables avec files de messages, event sourcing et patterns CQRS.', 'description_ar': 'خدمات مصغرة قابلة للتوسع مع طوابير رسائل ومصادر أحداث وأنماط CQRS.', 'icon_emoji': '📨', 'order': 3},
                ],
            },
            {
                'title_en': 'Cloud & DevOps',
                'title_fr': 'Cloud & DevOps',
                'title_ar': 'الحوسبة السحابية و DevOps',
                'subtitle_en': 'Automated infrastructure for zero-downtime operations',
                'subtitle_fr': 'Infrastructure automatisée pour des opérations sans interruption',
                'subtitle_ar': 'بنية تحتية آلية لعمليات بدون توقف',
                'description_en': 'Cloud infrastructure on AWS/GCP, automated CI/CD deployment pipelines, containerization with Docker, and 24/7 observability.',
                'description_fr': 'Infrastructures cloud sur AWS/GCP, pipelines CI/CD automatisés, conteneurisation Docker et observabilité continue.',
                'description_ar': 'بنية تحتية سحابية متطورة على AWS و GCP، أتمتة خطوط النشر CI/CD، حاويات Docker، ومراقبة أداء مستمرة على مدار الساعة.',
                'methodology_en': 'Infrastructure as Code (IaC) with Terraform and Ansible. GitOps workflow with automated rollbacks, blue-green deployments, and comprehensive monitoring with Prometheus/Grafana.',
                'methodology_fr': 'Infrastructure as Code (IaC) avec Terraform et Ansible. Workflow GitOps avec rollbacks automatisés et monitoring Prometheus/Grafana.',
                'methodology_ar': 'البنية التحتية كشفرة (IaC) مع Terraform و Ansible. سير عمل GitOps مع تراجعات آلية ومراقبة Prometheus/Grafana.',
                'deliverables_en': 'Cloud architecture design\nCI/CD pipeline setup\nDocker containerization\nInfrastructure as Code (Terraform)\nMonitoring & alerting (Prometheus/Grafana)\nDisaster recovery plan',
                'deliverables_fr': 'Design d\'architecture cloud\nConfiguration pipeline CI/CD\nConteneurisation Docker\nInfrastructure as Code (Terraform)\nMonitoring & alertes (Prometheus/Grafana)\nPlan de reprise après sinistre',
                'deliverables_ar': 'تصميم معمارية السحابة\nإعداد خطوط CI/CD\nحاويات Docker\nالبنية التحتية كشفرة (Terraform)\nمراقبة وتنبيهات (Prometheus/Grafana)\nخطة التعافي من الكوارث',
                'technologies': 'AWS, GCP, Docker, Kubernetes, Terraform, Ansible, GitHub Actions, Prometheus',
                'timeline': '2 — 8 Weeks',
                'icon': 'icon-cloud', 'is_featured': False, 'order': 6,
                'solutions': [
                    {'title_en': 'Cloud Migration', 'title_fr': 'Migration Cloud', 'title_ar': 'الهجرة السحابية', 'description_en': 'Seamless migration from on-premises to cloud with minimal downtime and data integrity guarantees.', 'description_fr': 'Migration fluide du on-premise vers le cloud avec temps d\'arrêt minimal et garantie d\'intégrité des données.', 'description_ar': 'هجرة سلسة من البنية المحلية إلى السحابة مع حد أدنى من التوقف وضمان سلامة البيانات.', 'icon_emoji': '☁️', 'order': 1},
                    {'title_en': 'CI/CD Automation', 'title_fr': 'Automatisation CI/CD', 'title_ar': 'أتمتة CI/CD', 'description_en': 'Automated build, test, and deployment pipelines that ship code to production multiple times per day.', 'description_fr': 'Pipelines automatisés de build, test et déploiement pour livrer du code en production plusieurs fois par jour.', 'description_ar': 'خطوط بناء واختبار ونشر آلية تنشر الكود في الإنتاج عدة مرات يوميًا.', 'icon_emoji': '🔄', 'order': 2},
                    {'title_en': '24/7 Monitoring', 'title_fr': 'Monitoring 24/7', 'title_ar': 'مراقبة على مدار الساعة', 'description_en': 'Comprehensive observability with custom dashboards, alerting, and incident response automation.', 'description_fr': 'Observabilité complète avec tableaux de bord personnalisés, alertes et automatisation de la réponse aux incidents.', 'description_ar': 'رصد شامل مع لوحات معلومات مخصصة وتنبيهات وأتمتة الاستجابة للحوادث.', 'icon_emoji': '📊', 'order': 3},
                ],
            },
        ]
        for svc_data in services_data:
            solutions = svc_data.pop('solutions', [])
            svc = Service.objects.create(**svc_data)
            for sol_data in solutions:
                ServiceSolution.objects.create(service=svc, **sol_data)
        self.stdout.write(f'  [OK] Created {len(services_data)} multilingual services with solutions')

        # ── 4. Project Categories ──
        ProjectCategory.objects.all().delete()
        cats_data = [
            ('Agro-Export', 'Agro-Export', 'الصناعات الغذائية والتصدير', 'agroexport'),
            ('HealthTech', 'HealthTech', 'الصحة الرقمية', 'healthtech'),
            ('Medical Lab', 'Laboratoire Médical', 'المختبر الطبي', 'medlab'),
            ('Food Industry', 'Industrie Alimentaire', 'الصناعات الغذائية', 'food'),
            ('E-Commerce', 'E-Commerce', 'التجارة الإلكترونية', 'ecommerce'),
            ('SaaS', 'SaaS', 'البرمجيات السحابية', 'saas'),
            ('Local Business', 'Commerce Local', 'الأعمال المحلية', 'local-business'),
            ('Construction', 'Construction', 'البناء والتشييد', 'construction'),
            ('Advertising', 'Publicité', 'الإعلان والدعاية', 'advertising'),
            ('Events & Spaces', 'Événements & Espaces', 'الفعاليات والمساحات', 'events'),
        ]
        cat_map = {}
        for n_en, n_fr, n_ar, slug in cats_data:
            c = ProjectCategory.objects.create(name_en=n_en, name_fr=n_fr, name_ar=n_ar, slug=slug)
            cat_map[slug] = c
        self.stdout.write(f'  [OK] Created {len(cats_data)} multilingual categories')

        # ── 5. Projects ──
        Project.objects.all().delete()
        projects_data = [
            {
                'title_en': 'MEDICENTERS PERFORMANCE',
                'title_fr': 'MEDICENTERS PERFORMANCE',
                'title_ar': 'منصة ميديسنترز بيرفورمانس',
                'slug': 'medicenters-performance',
                'cat_slug': 'healthtech',
                'd_en': 'Medical architecture, space fitting, and turnkey healthcare design platform with interactive 360° virtual tours.',
                'd_fr': 'Plateforme d\'aménagement et agencement d\'espaces médicaux professionnels à Tanger avec visites virtuelles 360° immersives.',
                'd_ar': 'منصة رائدة في تهيئة وتجهيز المساحات الطبية والعيادات في طنجة مع جولات افتراضية تفاعلية 360 درجة.',
                'seed': 'medicenters',
                'feat': True,
                'order': 1,
                'client': 'MEDICENTERS PERFORMANCE',
                'tech': 'Django, Bootstrap 5, Pannellum 360, JavaScript, i18n, PostgreSQL',
                'duration': '3 Months',
                'year': '2024',
                'live_url': 'https://medicenters.ma',
                'github_url': '',
                'challenge_en': 'Medical clinics and healthcare spaces require strict sanitary standards and specialized ergonomic layouts. The client needed a digital platform allowing doctors and healthcare investors to visualize turnkey clinic architectural transformations and navigate completed medical suites before commissioning work.',
                'challenge_fr': 'Les cliniques et cabinets médicaux exigent des normes sanitaires rigoureuses et des agencements ergonomiques spécifiques. Le client souhaitait une plateforme digitale permettant aux médecins et investisseurs de visualiser les transformations architecturales et d\'explorer les espaces en 360° avant le lancement des chantiers.',
                'challenge_ar': 'تتطلب العيادات والمراكز الطبية معايير صحية وهندسية دقيقة وتجهيزات خاصة. احتاج العميل إلى منصة رقمية تمكن الأطباء والمستثمرين من معاينة التصاميم الهندسية وجولات تفاعلية 360 درجة للعيادات قبل بدء أعمال التنفيذ.',
                'solution_en': 'We engineered a high-performance Django web platform integrating Pannellum for seamless 360° web-based virtual walkthroughs without heavy plugins. We built custom bilingual portfolio galleries, an interactive clinic quote estimator, and optimized image compression for lightning-fast loading across mobile and desktop.',
                'solution_fr': 'Nous avons développé une plateforme web Django haute performance intégrant Pannellum pour des visites 360° fluides sans plugin lourd. Nous avons conçu une galerie portfolio bilingue, un estimateur de devis interactif et optimisé la compression d\'image pour un chargement instantané.',
                'solution_ar': 'قمنا بهندسة وتطوير منصة ويب متطورة بالاعتماد على Django مع دمج تقنية Pannellum للجولات الافتراضية 360 درجة بسلاسة تامة. أضفنا معرض أعمال تفاعلي ثنائي اللغة، وحاسبة تقدير تكاليف العيادات، مع تسريع التحميل على الجوال.',
                'results_en': '+180% increase in medical consultation inquiries within 90 days of launch; 3.5x longer average session duration driven by interactive 360° immersive tours; 100% PageSpeed performance score.',
                'results_fr': '+180% d\'augmentation des demandes de consultation en 90 jours ; durée moyenne de session multipliée par 3,5 grâce aux visites 360° ; score de performance Google PageSpeed optimal.',
                'results_ar': 'زيادة طلبات الاستشارة الطبية بنسبة 180% خلال 90 يوماً؛ ومضاعفة مدة تصفح الزوار بـ 3.5 أضعاف بفضل الجولات التفاعلية 360؛ وأداء فائق السرعة على محركات البحث.',
                'quote_en': 'getNexiro delivered an immaculate digital platform that elevated our medical architecture studio above regional competitors. The 360 tours have been our best client acquisition tool.',
                'quote_fr': 'getNexiro a conçu une plateforme impeccable qui a propulsé notre cabinet d\'architecture médicale au premier plan. Les visites 360° sont devenues notre meilleur vecteur d\'acquisition.',
                'quote_ar': 'قدمت لنا getNexiro منصة رقمية استثنائية ميزت استوديو الهندسة الطبية الخاص بنا عن جميع المنافسين. الجولات الافتراضية أصبحت أقوى أداة لجذب العملاء.',
                'quote_author': 'Dr. M. Benjelloun',
                'quote_role': 'Managing Director, MEDICENTERS',
            },
            {
                'title_en': 'CAPERSMED Wholesale Export',
                'title_fr': 'CAPERSMED Export Agroalimentaire',
                'title_ar': 'منصة كابرز ميد للتصدير الدولي',
                'slug': 'capersmed-wholesale-export',
                'cat_slug': 'agroexport',
                'd_en': 'Global B2B agro-food export platform featuring multi-market internationalization across 9 languages, technical SEO, and BRC/IFS certification showcases.',
                'd_fr': 'Plateforme B2B mondiale d\'exportation agroalimentaire avec internationalisation en 9 langues, SEO technique et mise en avant des certifications BRC/IFS.',
                'd_ar': 'منصة تصدير دولية B2B للصناعات الغذائية تدعم 9 لغات عالمية مع تحسين محركات البحث المتقدم واستعراض شهادات الجودة العالمية BRC و IFS.',
                'seed': 'capersmed',
                'feat': True,
                'order': 2,
                'client': 'CAPERSMED SARL',
                'tech': 'Django, Multilingual (9 languages), Technical SEO, Schema.org, Cloudflare CDN',
                'duration': '4 Months',
                'year': '2024',
                'live_url': 'https://capersmed.com',
                'github_url': '',
                'challenge_en': 'Exporting Moroccan specialty capers, olives, and condiments to 25+ countries required an authoritative international presence complying with BRCGS and IFS food safety standards, with search engine discoverability across European, American, and Asian markets.',
                'challenge_fr': 'L\'exportation de câpres, olives et condiments marocains vers plus de 25 pays nécessitait une présence internationale prestigieuse conforme aux normes BRCGS et IFS, avec un référencement multilingue ciblé sur l\'Europe, l\'Amérique et l\'Asie.',
                'challenge_ar': 'تصدير الكبر والزيتون والتوابل المغربية إلى أكثر من 25 دولة تطلب منصة دولية رفيعة المستوى متوافقة مع معايير سلامة الأغذية BRCGS و IFS، وظهوراً متصدراً في محركات البحث العالمية.',
                'solution_en': 'Architected a multi-region internationalized platform in 9 languages with localized hreflang tags, dynamic product specifications, interactive packaging options, and technical schema markup for wholesale agricultural trade.',
                'solution_fr': 'Architecture d\'une plateforme multirégionale en 9 langues avec balises hreflang localisées, fiches techniques interactives, packaging sur mesure et balisage Schema.org pour le commerce B2B.',
                'solution_ar': 'تطوير بنية تحتية برمجية تدعم 9 لغات مع وسوم التوطين الجغرافي hreflang، ومواصفات تفاعلية للمنتجات الزراعية، وتوافق تام مع محركات البحث العالمية.',
                'results_en': 'Generated qualified wholesale export RFQs from importers across Germany, the UK, the US, and Japan; ranked in top 3 Google search results for wholesale Mediterranean capers.',
                'results_fr': 'Génération d\'appels d\'offres B2B qualifiés d\'importateurs en Allemagne, au Royaume-Uni et aux USA ; positionnement dans le top 3 Google mondial.',
                'results_ar': 'استقطاب طلبات توريد B2B كبرى من مستوردين في ألمانيا وبريطانيا وأمريكا واليابان، وتصدر المراتب الثلاث الأولى عالمياً في محركات البحث.',
                'quote_en': 'The multilingual export platform built by getNexiro opened direct distribution channels for our agro products in major international supermarkets.',
                'quote_fr': 'La plateforme d\'export développée par getNexiro nous a ouvert des canaux directs auprès des grands distributeurs internationaux.',
                'quote_ar': 'فتحت لنا المنصة التي بنتها getNexiro قنوات توزيع مباشرة مع كبرى سلاسل التوزيع والمستوردين في مختلف دول العالم.',
                'quote_author': 'K. Alami',
                'quote_role': 'Export Director, CAPERSMED',
            },
            {
                'title_en': 'Laboratoire International Tanger',
                'title_fr': 'Laboratoire International de Tanger',
                'title_ar': 'المختبر الدولي للتحاليل الطبية بطنجة',
                'slug': 'laboratoire-international-tanger',
                'cat_slug': 'medlab',
                'd_en': 'Medical laboratory platform with online results portal, appointment booking, multilingual support, and SEO-optimized health blog.',
                'd_fr': 'Plateforme de laboratoire d\'analyses médicales avec portail de résultats en ligne, prise de rendez-vous, support multilingue et blog santé optimisé SEO.',
                'd_ar': 'منصة مختبر التحاليل الطبية مع بوابة نتائج إلكترونية وحجز مواعيد ودعم متعدد اللغات ومدونة صحية محسّنة لمحركات البحث.',
                'seed': 'laboratoire',
                'feat': True,
                'order': 3,
                'client': 'Laboratoire International de Tanger',
                'tech': 'Django, Bootstrap 5, i18n (FR/AR), Medical Blog CMS, Patient Portal API',
                'duration': '2.5 Months',
                'year': '2024',
                'live_url': '',
                'github_url': '',
                'challenge_en': 'Patients and healthcare professionals needed a frictionless, secure channel to prepare for diagnostic tests, book home sampling appointments, and access health guidance without calling the front desk.',
                'challenge_fr': 'Les patients et praticiens avaient besoin d\'un canal sécurisé et fluide pour préparer leurs analyses, réserver des prélèvements à domicile et consulter les recommandations de santé.',
                'challenge_ar': 'احتاج المرضى والأطباء إلى قناة رقمية آمنة وسهلة لمعرفة إرشادات التحاليل المخبرية، وحجز مواعيد أخذ العينات المنزلية، ومتابعة الفحوصات الطبية بكل يسر.',
                'solution_en': 'Built an intuitive bilingual healthcare portal featuring an exhaustive searchable directory of medical tests with fasting instructions, home blood-drawing appointment request workflows, and an evidence-based medical blog.',
                'solution_fr': 'Conception d\'un portail bilingue avec annuaire de recherche d\'analyses médicales et conditions de jeûne, module de rendez-vous à domicile et blog médical validé scientifiquement.',
                'solution_ar': 'بناء منصة طبية ثنائية اللغة تضم دليلاً شاملاً للتحاليل الطبية مع شروط الصيام والتحضير، ونظام حجز مرن للعينات المنزلية، ومدونة طبية توعوية معتمدة.',
                'results_en': 'Reduced reception phone queue volume by 42%; over 1,200 monthly online appointment requests; ranked #1 in Tangier for clinical biology and medical laboratory queries.',
                'results_fr': 'Réduction de 42% des appels au secrétariat ; plus de 1 200 demandes en ligne par mois ; 1er sur Google pour les analyses médicales à Tanger.',
                'results_ar': 'تخفيف ضغط المكالات على الاستقبال بنسبة 42%؛ وأكثر من 1200 موعد شهري عبر الإنترنت؛ وتصدر نتائج البحث في طنجة لمختبرات التحاليل الطبية.',
                'quote_en': 'Our patient intake and home sampling operations became dramatically more efficient thanks to getNexiro\'s user-centric engineering.',
                'quote_fr': 'La prise en charge de nos patients et nos tournées à domicile sont devenues d\'une efficacité remarquable grâce au travail de getNexiro.',
                'quote_ar': 'أصبحت تجربة مرضانا وإدارة المواعيد المنزلية في غاية الانسيابية والكفاءة بفضل التميز التقني لفريق getNexiro.',
                'quote_author': 'Dr. S. Tazi',
                'quote_role': 'Biologiste Directeur, Laboratoire International',
            },
            {
                'title_en': 'Vinaigre du Maroc',
                'title_fr': 'Vinaigre du Maroc',
                'title_ar': 'خل المغرب للتصدير',
                'slug': 'vinaigre-du-maroc',
                'cat_slug': 'food',
                'd_en': 'B2B export platform for premium Moroccan vinegar and condiments with international BRC/IFS/Halal certifications and multilingual product catalog.',
                'd_fr': 'Plateforme d\'exportation B2B de vinaigre et condiments premium marocains avec certifications internationales BRC/IFS/Halal et catalogue produits multilingue.',
                'd_ar': 'منصة تصدير B2B للخل والتوابل المغربية الفاخرة مع شهادات الجودة الدولية BRC/IFS/حلال وكتالوج منتجات متعدد اللغات.',
                'seed': 'vinaigre',
                'feat': True,
                'order': 4,
                'client': 'Vinaigre du Maroc SARL',
                'tech': 'Django, Bootstrap 5, SEO Architecture, Multilingual Catalog, WebP Optimization',
                'duration': '2 Months',
                'year': '2023',
                'live_url': '',
                'github_url': '',
                'challenge_en': 'Presenting industrial-grade vinegar fermentation capabilities, organic food certifications, and bulk shipping container configurations to large food conglomerates across Europe and Africa.',
                'challenge_fr': 'Valoriser les capacités industrielles de fermentation de vinaigre, les certifications bio et les configurations d\'expédition en gros auprès des distributeurs européens et africains.',
                'challenge_ar': 'إبراز القدرات الصناعية المتقدمة في تخمير وتصنيع الخل الطبيعي، والشهادات العضوية، وخيارات الشحن بالحاويات للشركات الغذائية الكبرى.',
                'solution_en': 'Designed and shipped a modern industrial product catalog with interactive bottle and IBC container volume specs, laboratory purity analyses, and multilingual contact funnels for international distributors.',
                'solution_fr': 'Création d\'un catalogue industriel moderne avec spécifications techniques des contenants (bouteilles, fûts, cuves IBC), analyses de pureté et tunnels de contact multilingues.',
                'solution_ar': 'تصميم كتالوج صناعي تفاعلي يوضح سعات التعبئة (من القنينات الاستهلاكية إلى خزانات IBC الكبرى) مع التحاليل المخبرية ونماذج تواصل متعددة اللغات.',
                'results_en': 'Secured 3 major private-label manufacturing contracts in France and West Africa within the first quarter post-launch.',
                'results_fr': 'Signature de 3 contrats majeurs de fabrication en marque blanche en France et en Afrique de l\'Ouest dès le premier trimestre.',
                'results_ar': 'إبرام 3 عقود تصنيع كبرى بعلامات تجارية خاصة في فرنسا ودول غرب إفريقيا في الربع الأول بعد الإطلاق.',
                'quote_en': 'getNexiro gave our traditional manufacturing business a sleek, high-trust digital identity that commands respect in international food expos.',
                'quote_fr': 'getNexiro a doté notre usine d\'une vitrine technologique prestigieuse qui inspire une confiance immédiate lors des salons internationaux.',
                'quote_ar': 'منحت getNexiro مصنعنا هوية رقمية عالمية رفيعة المستوى تحظى بتقدير وثقة كبار المستوردين في المعارض الدولية.',
                'quote_author': 'O. Chraibi',
                'quote_role': 'CEO, Vinaigre du Maroc',
            },
            {
                'title_en': 'Diwan Atlas — Customs SaaS',
                'title_fr': 'Diwan Atlas — Facturation Douane',
                'title_ar': 'ديوان أطلس — منصة الفوترة الجمركية',
                'slug': 'diwan-atlas-customs-saas',
                'cat_slug': 'saas',
                'd_en': 'Bespoke SaaS invoicing and regulatory clearance platform engineered for licensed customs brokers and transit agents in Morocco, featuring automated port fee computation, VAT breakdown, and bilingual FR/AR interface.',
                'd_fr': 'Plateforme SaaS métier de facturation et de gestion des dossiers douaniers conçue pour les agents en douane et transitaires au Maroc, avec calcul automatisé des débours, TVA douanière et interface bilingue FR/AR.',
                'd_ar': 'منصة سحابية متقدمة لفوترة وإدارة الملفات الجمركية مصممة لوكلاء ومعشري الجمارك في المغرب، تتميز باحتساب آلي للرسوم وتتبع الفواتير والامتثال الضريبي بواجهة ثنائية اللغة.',
                'seed': 'diwanatlas',
                'feat': True,
                'order': 5,
                'client': 'Cabinet de Transit & Douane (Confidentiel)',
                'tech': 'Next.js, TypeScript, Tailwind CSS, PostgreSQL, Python, PDF Generation Engine',
                'duration': '5 Months',
                'year': '2025',
                'live_url': 'https://github.com/Schneider-sizeof/Diouan-atlass',
                'github_url': 'https://github.com/Schneider-sizeof/Diouan-atlass',
                'challenge_en': 'Customs clearance in Morocco involves complex regulatory calculations: BADR declarations, port logistics fees, maritime demurrage, and intricate VAT exemptions on customs disbursements. Manual invoicing led to calculation errors, delayed port releases, and reconciliation overhead.',
                'challenge_fr': 'Le dédouanement au Maroc implique des calculs réglementaires complexes : déclarations BADR, frais portuaires, surestaries maritimes et gestion rigoureuse de la TVA sur débours. La facturation manuelle engendrait des erreurs et des retards de dédouanement.',
                'challenge_ar': 'تعتمد المعاملات الجمركية في المغرب على حسابات دقيقة ومعقدة: تصاريح نظام بدر، رسوم الموانئ، غرامات التأخير، ومعالجة ضريبة القيمة المضافة على المصاريف الجمركية. الفوترة اليدوية كانت تسبب أخطاء محاسبية وتأخيراً في الإفراج الجمركي.',
                'solution_en': 'We engineered a bespoke, secure web application with automated Port & Customs tariff calculation engines, multi-currency conversion, bilingual PDF invoice generation compliant with Moroccan DGI regulations, and a client tracking portal.',
                'solution_fr': 'Développement d\'une application web sur mesure avec moteur de calcul automatisé des tarifs douaniers et portuaires, génération de factures PDF conformes aux normes DGI marocaines et portail de suivi client.',
                'solution_ar': 'بناء منصة برمجية مخصصة بمحرك احتساب آلي للرسوم الجمركية والمينائية، وتوليد فواتير رسمية متوافقة مع متطلبات إدارة الضرائب DGI، وبوابة لتتبع المعاملات.',
                'results_en': 'Cut customs dossier billing cycle time from 3 days to under 15 minutes; eliminated 100% of tariff calculation discrepancies; processed over 15,000 import/export declaration lines seamlessly.',
                'results_fr': 'Cycle de facturation réduit de 3 jours à moins de 15 minutes ; élimination totale des erreurs de calcul ; plus de 15 000 lignes de déclarations traitées avec succès.',
                'results_ar': 'تقليص وقت معالجة الفواتير الجمركية من 3 أيام إلى أقل من 15 دقيقة؛ والقضاء الكامل على أخطاء الحسابات؛ ومعالجة أكثر من 15,000 بند جمركي بنجاح.',
                'quote_en': 'Diwan Atlas transformed our customs agency into a modern, hyper-efficient operation. Our clearance teams and accountants save hours of manual calculation every single day.',
                'quote_fr': 'Diwan Atlas a transformé notre agence en une structure moderne et ultra-performante. Nos déclarants et comptables économisent des heures de travail chaque jour.',
                'quote_ar': 'أحدثت منصة ديوان أطلس نقلة نوعية في وكالتنا الجمركية. يوفر فريق المعشرين والمحاسبين ساعات طويلة من العمل اليدوي يومياً وبدقة متناهية.',
                'quote_author': 'A. El Fassi',
                'quote_role': 'Directeur des Opérations, Cabinet de Douane',
            },
            # ── 6 Real Client Websites ──
            {
                'title_en': 'StoreTanger — Custom Curtains & Blinds',
                'title_fr': 'StoreTanger — Rideaux & Stores Sur Mesure',
                'title_ar': 'ستور طنجة — ستائر ومظلات حسب الطلب',
                'slug': 'storetanger',
                'cat_slug': 'local-business',
                'd_en': 'Premium landing page for a bespoke curtains and blinds manufacturer in Tangier, featuring WhatsApp lead generation, full SEO optimization, and a luxurious dark-themed UI.',
                'd_fr': 'Landing page premium pour un fabricant de rideaux et stores sur mesure à Tanger, avec génération de leads WhatsApp, SEO complet et design luxueux sombre.',
                'd_ar': 'صفحة هبوط احترافية لمصنّع ستائر ومظلات حسب الطلب في طنجة، مع توليد العملاء عبر واتساب وتحسين SEO كامل وتصميم فاخر.',
                'seed': 'storetanger',
                'feat': True,
                'order': 5,
                'client': 'StoreTanger',
                'tech': 'HTML5, CSS3, JavaScript, SEO, Schema.org, WhatsApp API',
                'duration': '2 Weeks',
                'year': '2025',
                'live_url': 'https://storetanger.com',
                'github_url': '',
                'challenge_en': 'The client needed a high-converting single-page website that would rank for "rideaux Tanger" and "stores sur mesure Tanger" on Google, while converting visitors into WhatsApp inquiries with minimal friction.',
                'challenge_fr': 'Le client avait besoin d\'un site one-page ultra-performant bien positionné sur "rideaux Tanger" et "stores sur mesure Tanger", convertissant les visiteurs en demandes WhatsApp avec un minimum de friction.',
                'challenge_ar': 'احتاج العميل إلى موقع صفحة واحدة عالي التحويل يتصدر نتائج "ستائر طنجة" و"مظلات حسب الطلب طنجة" على جوجل، مع تحويل الزوار إلى استفسارات واتساب بسلاسة.',
                'solution_en': 'We designed a visually stunning dark-themed landing page with elegant typography, FAQ accordion, interactive product galleries, and integrated WhatsApp CTA buttons. Full JSON-LD structured data and comprehensive on-page SEO.',
                'solution_fr': 'Nous avons conçu une landing page sombre élégante avec typographie raffinée, FAQ accordéon, galeries produits interactives et boutons CTA WhatsApp intégrés. Données structurées JSON-LD et SEO on-page complet.',
                'solution_ar': 'صممنا صفحة هبوط أنيقة بتصميم داكن مع خطوط فاخرة وأسئلة شائعة تفاعلية ومعارض منتجات ديناميكية وأزرار واتساب. بيانات منظمة JSON-LD وتحسين SEO شامل.',
                'results_en': 'Ranked #1 on Google for "rideaux Tanger" within 30 days; 85% of leads come through WhatsApp; 95+ PageSpeed score; 3x increase in monthly client inquiries.',
                'results_fr': 'Classé #1 sur Google pour "rideaux Tanger" en 30 jours ; 85% des leads via WhatsApp ; score PageSpeed 95+ ; multiplication par 3 des demandes mensuelles.',
                'results_ar': 'المركز الأول على جوجل لـ"ستائر طنجة" خلال 30 يوماً؛ 85% من العملاء عبر واتساب؛ نتيجة PageSpeed أكثر من 95؛ زيادة 3 أضعاف في الاستفسارات.',
                'quote_en': 'getNexiro built us a website that looks premium and brings real customers through Google and WhatsApp every single day.',
                'quote_fr': 'getNexiro nous a créé un site premium qui nous amène de vrais clients via Google et WhatsApp chaque jour.',
                'quote_ar': 'صمم لنا getNexiro موقعاً فاخراً يجلب عملاء حقيقيين عبر جوجل وواتساب يومياً.',
                'quote_author': 'Propriétaire',
                'quote_role': 'StoreTanger, Tanger',
            },
            {
                'title_en': 'AluminiumTanger — Glass & Aluminium',
                'title_fr': 'AluminiumTanger — Verre & Aluminium',
                'title_ar': 'ألمنيوم طنجة — الزجاج والألمنيوم',
                'slug': 'aluminiumtanger',
                'cat_slug': 'construction',
                'd_en': 'Professional showcase website for a glass and aluminium specialist in Tangier — tempered glass, partitions, double glazing, shower enclosures, and custom accordion glass.',
                'd_fr': 'Site vitrine professionnel pour un spécialiste du verre et aluminium à Tanger — verre trempé, cloisons vitrées, double vitrage, séparations douche et vitres en accordéon.',
                'd_ar': 'موقع عرض احترافي لمتخصص في الزجاج والألمنيوم في طنجة — زجاج مقوى، فواصل زجاجية، زجاج مزدوج، فواصل دوش وزجاج أكورديون.',
                'seed': 'aluminiumtanger',
                'feat': True,
                'order': 6,
                'client': 'Aluminium Tanger',
                'tech': 'HTML5, CSS3, JavaScript, Local SEO, Schema.org, hreflang',
                'duration': '2 Weeks',
                'year': '2025',
                'live_url': 'https://aluminiumtanger.com',
                'github_url': '',
                'challenge_en': 'The aluminium and glass workshop needed a modern digital presence to compete with local artisans, showcasing their premium products with geo-targeted SEO for Tangier and northern Morocco.',
                'challenge_fr': 'L\'atelier d\'aluminium et verre avait besoin d\'une présence digitale moderne pour se démarquer, avec un SEO géo-ciblé sur Tanger et le nord du Maroc.',
                'challenge_ar': 'احتاج ورشة الألمنيوم والزجاج إلى حضور رقمي عصري للتنافس مع الحرفيين المحليين، مع تحسين محركات البحث الجغرافي لطنجة وشمال المغرب.',
                'solution_en': 'Built a sleek, fast-loading website with product service showcases, interactive contact forms, WhatsApp integration, and comprehensive local SEO with geo meta tags and hreflang for French-speaking markets.',
                'solution_fr': 'Conception d\'un site rapide et élégant avec vitrines produits, formulaires de contact interactifs, intégration WhatsApp et SEO local complet avec balises géo et hreflang.',
                'solution_ar': 'تطوير موقع أنيق وسريع التحميل مع عرض المنتجات ونماذج اتصال تفاعلية ودمج واتساب وتحسين SEO محلي شامل.',
                'results_en': 'Top 3 Google rankings for "aluminium Tanger" and "cloisons vitrées Tanger"; significant increase in quote requests from architects and property developers.',
                'results_fr': 'Top 3 Google pour "aluminium Tanger" et "cloisons vitrées Tanger" ; forte augmentation des demandes de devis d\'architectes et promoteurs.',
                'results_ar': 'تصنيف ضمن أفضل 3 على جوجل لـ"ألمنيوم طنجة" و"فواصل زجاجية طنجة"؛ زيادة كبيرة في طلبات العروض.',
                'quote_en': 'Our website finally matches the quality of our craftsmanship. getNexiro understood exactly what we needed.',
                'quote_fr': 'Notre site reflète enfin la qualité de notre savoir-faire. getNexiro a parfaitement compris nos besoins.',
                'quote_ar': 'موقعنا أخيراً يعكس جودة حرفيتنا. getNexiro فهم تماماً ما نحتاجه.',
                'quote_author': 'Gérant',
                'quote_role': 'Aluminium Tanger',
            },
            {
                'title_en': 'ALPSCAFFOLD — Scaffolding & Equipment Rental',
                'title_fr': 'ALPSCAFFOLD — Location Échafaudage & Équipements',
                'title_ar': 'ALPSCAFFOLD — تأجير السقالات والمعدات',
                'slug': 'alpscaffold-echafaudage',
                'cat_slug': 'construction',
                'd_en': 'Lead-generation website for scaffolding rental, electric suspended platforms, and Manitou telescopic handlers in Tangier — with instant WhatsApp quoting.',
                'd_fr': 'Site de génération de leads pour la location d\'échafaudages, plateformes électriques suspendues et chariots télescopiques Manitou à Tanger — devis WhatsApp instantané.',
                'd_ar': 'موقع توليد عملاء لتأجير السقالات والمنصات الكهربائية المعلقة ورافعات مانيتو التلسكوبية في طنجة — عروض أسعار فورية عبر واتساب.',
                'seed': 'alpscaffold',
                'feat': False,
                'order': 7,
                'client': 'ALPSCAFFOLD',
                'tech': 'HTML5, CSS3, JavaScript, Local SEO, WhatsApp API, Schema.org',
                'duration': '10 Days',
                'year': '2025',
                'live_url': 'https://locationechafaudagetanger.com',
                'github_url': '',
                'challenge_en': 'A construction equipment rental company needed an online presence targeting contractors and builders searching for scaffolding, electric platforms, and Manitou cranes in Tangier.',
                'challenge_fr': 'Une société de location de matériel BTP avait besoin d\'une présence en ligne ciblant les entrepreneurs recherchant des échafaudages et chariots Manitou à Tanger.',
                'challenge_ar': 'شركة تأجير معدات بناء احتاجت لحضور رقمي يستهدف المقاولين الباحثين عن سقالات ومنصات كهربائية ورافعات مانيتو في طنجة.',
                'solution_en': 'Designed a conversion-focused website with clear pricing (from 50 DH/level/day), instant WhatsApp quote buttons, bilingual Arabic/French SEO targeting all Tangier neighborhoods, and service area coverage maps.',
                'solution_fr': 'Conception d\'un site axé conversion avec tarifs clairs (à partir de 50 DH/étage/jour), boutons devis WhatsApp instantanés et SEO bilingue arabe/français ciblant tous les quartiers de Tanger.',
                'solution_ar': 'تصميم موقع محوره التحويل بأسعار واضحة (ابتداءً من 50 درهم/طابق/يوم)، وأزرار عروض أسعار واتساب فورية، وتحسين محركات بحث عربي/فرنسي.',
                'results_en': 'Ranked #1 for "location échafaudage Tanger"; 70% of inquiries come via WhatsApp within the first month of launch.',
                'results_fr': 'Classé #1 pour "location échafaudage Tanger" ; 70% des demandes via WhatsApp dès le premier mois.',
                'results_ar': 'المركز الأول لـ"تأجير سقالات طنجة"؛ 70% من الاستفسارات عبر واتساب في الشهر الأول.',
                'quote_en': 'Simple, effective, and it works. We get calls and WhatsApp messages from new clients every week thanks to getNexiro.',
                'quote_fr': 'Simple, efficace, et ça marche. Nous recevons des appels et messages WhatsApp de nouveaux clients chaque semaine grâce à getNexiro.',
                'quote_ar': 'بسيط وفعال ويعمل. نتلقى مكالمات ورسائل واتساب من عملاء جدد كل أسبوع بفضل getNexiro.',
                'quote_author': 'Directeur',
                'quote_role': 'ALPSCAFFOLD, Tanger',
            },
            {
                'title_en': 'Écran LED Tanger — LED Screen Solutions',
                'title_fr': 'Écran LED Tanger — Solutions Écrans LED',
                'title_ar': 'شاشات LED طنجة — حلول الشاشات الرقمية',
                'slug': 'ecran-led-tanger',
                'cat_slug': 'advertising',
                'd_en': 'Showcase website for LED screen sales, rental, and installation in Tangier — featuring video walls, LED totems, and dynamic digital signage solutions.',
                'd_fr': 'Site vitrine pour la vente, location et installation d\'écrans LED à Tanger — murs LED, totems et affichage dynamique.',
                'd_ar': 'موقع عرض لبيع وتأجير وتركيب شاشات LED في طنجة — جدران LED وأعمدة إعلانية ولافتات رقمية.',
                'seed': 'ecranled',
                'feat': True,
                'order': 8,
                'client': 'Écran LED Tanger',
                'tech': 'HTML5, CSS3, JavaScript, SEO, Schema.org, Performance Optimization',
                'duration': '2 Weeks',
                'year': '2025',
                'live_url': 'https://ecranledtanger.com',
                'github_url': '',
                'challenge_en': 'An LED technology company needed a visually impactful website that demonstrates the power and quality of LED screens through its own design, while driving B2B and event inquiries.',
                'challenge_fr': 'Une entreprise technologique LED avait besoin d\'un site visuellement percutant démontrant la puissance des écrans LED à travers son propre design, tout en générant des demandes B2B.',
                'challenge_ar': 'شركة تقنية LED احتاجت لموقع بصري مؤثر يعرض قوة وجودة شاشات LED من خلال تصميمه، مع جذب استفسارات الشركات والفعاليات.',
                'solution_en': 'Created a high-impact website with dark visual aesthetics reflecting LED technology, product catalogs for indoor/outdoor screens and totems, instant quote system, and SEO targeting "écran LED Tanger" and related keywords.',
                'solution_fr': 'Création d\'un site à fort impact visuel avec esthétique sombre reflétant la technologie LED, catalogues indoor/outdoor, système de devis instantané et SEO ciblé.',
                'solution_ar': 'إنشاء موقع بتأثير بصري عالٍ يعكس تقنية LED، مع كتالوجات شاشات داخلية/خارجية، ونظام عروض أسعار فوري وتحسين محركات البحث.',
                'results_en': 'Page 1 Google rankings for "écran LED Tanger" and "location écran LED Tanger"; 50% increase in B2B quote requests within first quarter.',
                'results_fr': 'Page 1 Google pour "écran LED Tanger" et "location écran LED Tanger" ; +50% de demandes de devis B2B au premier trimestre.',
                'results_ar': 'الصفحة الأولى على جوجل لـ"شاشات LED طنجة"؛ زيادة 50% في طلبات عروض الأسعار B2B في الربع الأول.',
                'quote_en': 'getNexiro created a website as dynamic and impactful as our LED screens. It has become our most powerful sales tool.',
                'quote_fr': 'getNexiro a créé un site aussi dynamique et percutant que nos écrans LED. C\'est devenu notre outil commercial le plus puissant.',
                'quote_ar': 'أنشأ getNexiro موقعاً ديناميكياً ومؤثراً كشاشاتنا LED. أصبح أقوى أداة مبيعات لدينا.',
                'quote_author': 'Gérant',
                'quote_role': 'Écran LED Tanger',
            },
            {
                'title_en': 'Panneau Publicitaire Tanger — Signage & LED Signs',
                'title_fr': 'Panneau Publicitaire Tanger — Enseignes & Panneaux LED',
                'title_ar': 'لوحات إعلانية طنجة — لافتات وإعلانات LED',
                'slug': 'panneau-publicitaire-tanger',
                'cat_slug': 'advertising',
                'd_en': 'Professional website for an advertising signage manufacturer — custom LED signs, light boxes, totems, neon signs, and channel letters in Tangier.',
                'd_fr': 'Site professionnel pour un fabricant de signalétique publicitaire — enseignes LED, caissons lumineux, totems, néons et lettres boîtières à Tanger.',
                'd_ar': 'موقع احترافي لمصنّع لافتات إعلانية — لافتات LED وصناديق مضيئة وأعمدة إعلانية ونيون وحروف بارزة في طنجة.',
                'seed': 'panneau',
                'feat': False,
                'order': 9,
                'client': 'Panneau Publicitaire Tanger',
                'tech': 'HTML5, CSS3, JavaScript, Local SEO, WhatsApp API, Schema.org',
                'duration': '10 Days',
                'year': '2025',
                'live_url': 'https://panneaupublicitairetanger.com',
                'github_url': '',
                'challenge_en': 'A signage workshop needed a professional online presence to attract businesses, shops, and event organizers looking for custom LED signs and advertising panels in Tangier.',
                'challenge_fr': 'Un atelier d\'enseignes avait besoin d\'une présence professionnelle pour attirer les commerces et organisateurs d\'événements cherchant des panneaux publicitaires sur mesure à Tanger.',
                'challenge_ar': 'ورشة لافتات احتاجت حضوراً رقمياً احترافياً لجذب التجار ومنظمي الفعاليات الباحثين عن لوحات إعلانية مخصصة في طنجة.',
                'solution_en': 'Developed a product-focused website with detailed service categories (LED signs, light boxes, neon, totems, channel letters), portfolio gallery, instant WhatsApp CTA, and local SEO targeting Tangier neighborhoods.',
                'solution_fr': 'Développement d\'un site centré produits avec catégories détaillées (enseignes LED, caissons, néons, totems, lettres), galerie portfolio, CTA WhatsApp et SEO local ciblé.',
                'solution_ar': 'تطوير موقع يركز على المنتجات مع فئات خدمات مفصلة (لافتات LED، صناديق مضيئة، نيون، أعمدة)، ومعرض أعمال وأزرار واتساب وSEO محلي.',
                'results_en': 'Ranked top 3 for "panneau publicitaire Tanger" and "enseigne LED Tanger"; consistent flow of B2B and retail client inquiries.',
                'results_fr': 'Top 3 pour "panneau publicitaire Tanger" et "enseigne LED Tanger" ; flux constant de demandes B2B et retail.',
                'results_ar': 'تصنيف ضمن أفضل 3 لـ"لوحات إعلانية طنجة" و"لافتات LED طنجة"؛ تدفق مستمر من استفسارات العملاء.',
                'quote_en': 'getNexiro gave us a website that truly represents our craft. New clients find us on Google every day now.',
                'quote_fr': 'getNexiro nous a donné un site qui représente vraiment notre métier. De nouveaux clients nous trouvent sur Google chaque jour.',
                'quote_ar': 'منحنا getNexiro موقعاً يعكس حرفيتنا. عملاء جدد يجدوننا على جوجل يومياً.',
                'quote_author': 'Propriétaire',
                'quote_role': 'Panneau Publicitaire Tanger',
            },
            {
                'title_en': 'Salle de Formation Tanger — Training & Event Space',
                'title_fr': 'Salle de Formation Tanger — Espace Formation & Événementiel',
                'title_ar': 'قاعة التكوين طنجة — فضاء تدريب وفعاليات',
                'slug': 'salle-formation-tanger',
                'cat_slug': 'events',
                'd_en': 'Booking-focused website for a professional training room and event space in Valfleuri, Tangier — meeting rooms, workshops, reception areas, and networking spaces.',
                'd_fr': 'Site de réservation pour une salle de formation et espace événementiel à Valfleuri, Tanger — réunions, ateliers, réception et espaces networking.',
                'd_ar': 'موقع حجوزات لقاعة تدريب وفضاء فعاليات في فال فلوري، طنجة — قاعات اجتماعات وورش عمل ومساحات استقبال وتواصل.',
                'seed': 'salleformation',
                'feat': False,
                'order': 10,
                'client': 'Salle de Formation Tanger',
                'tech': 'HTML5, CSS3, JavaScript, Local SEO, WhatsApp Booking, Schema.org',
                'duration': '10 Days',
                'year': '2025',
                'live_url': 'https://salledeformationtanger.com',
                'github_url': '',
                'challenge_en': 'A training and event space near Iberia, Tangier, needed a digital presence to attract corporate trainers, coaches, and businesses looking for equipped rooms for up to 12 people.',
                'challenge_fr': 'Un espace de formation et événementiel près d\'Iberia à Tanger avait besoin d\'une présence digitale pour attirer formateurs, coachs et entreprises cherchant des salles équipées.',
                'challenge_ar': 'فضاء تدريب وفعاليات قرب إيبيريا في طنجة احتاج لحضور رقمي لجذب المدربين والشركات الباحثة عن قاعات مجهزة.',
                'solution_en': 'Created an elegant booking-focused website highlighting the space\'s amenities (WiFi, AC, projector, coffee included), room configurations, pricing, and instant WhatsApp reservation system with local SEO.',
                'solution_fr': 'Création d\'un site élégant axé réservation mettant en avant les équipements (WiFi, climatisation, vidéoprojecteur, café inclus), configurations de salles et réservation WhatsApp instantanée.',
                'solution_ar': 'إنشاء موقع أنيق يركز على الحجز يبرز التجهيزات (واي فاي، تكييف، جهاز عرض، قهوة) وتكوينات القاعات ونظام حجز واتساب فوري.',
                'results_en': 'Fully booked within the first month of launch; ranked #1 for "salle de formation Tanger" and "location salle Valfleuri"; 90% of bookings via WhatsApp.',
                'results_fr': 'Complet dès le premier mois ; classé #1 pour "salle de formation Tanger" et "location salle Valfleuri" ; 90% des réservations via WhatsApp.',
                'results_ar': 'حجز كامل في الشهر الأول؛ المركز الأول لـ"قاعة تدريب طنجة"؛ 90% من الحجوزات عبر واتساب.',
                'quote_en': 'Our space was unknown before getNexiro built our website. Now we are fully booked every week and clients find us on Google.',
                'quote_fr': 'Notre espace était inconnu avant que getNexiro crée notre site. Maintenant nous sommes complets chaque semaine.',
                'quote_ar': 'كان فضاءنا مجهولاً قبل أن يبني getNexiro موقعنا. الآن نحن محجوزون بالكامل كل أسبوع.',
                'quote_author': 'Responsable',
                'quote_role': 'Salle de Formation, Valfleuri Tanger',
            },
        ]

        created_projects = 0
        for pdata in projects_data:
            cat = cat_map.get(pdata['cat_slug'])
            seed = pdata['seed']
            img = get_image_file('projects', seed, f'{seed}.jpg', f'https://picsum.photos/seed/{seed}/600/400')

            p = Project(
                title_en=pdata['title_en'],
                title_fr=pdata['title_fr'],
                title_ar=pdata['title_ar'],
                slug=pdata['slug'],
                category=cat,
                description_en=pdata['d_en'],
                description_fr=pdata['d_fr'],
                description_ar=pdata['d_ar'],
                client_name=pdata['client'],
                technologies=pdata['tech'],
                duration=pdata.get('duration', '3 Months'),
                year=pdata.get('year', '2025'),
                live_url=pdata.get('live_url', ''),
                github_url=pdata.get('github_url', ''),
                challenge_en=pdata.get('challenge_en', ''),
                challenge_fr=pdata.get('challenge_fr', ''),
                challenge_ar=pdata.get('challenge_ar', ''),
                solution_en=pdata.get('solution_en', ''),
                solution_fr=pdata.get('solution_fr', ''),
                solution_ar=pdata.get('solution_ar', ''),
                results_en=pdata.get('results_en', ''),
                results_fr=pdata.get('results_fr', ''),
                results_ar=pdata.get('results_ar', ''),
                client_feedback_quote_en=pdata.get('quote_en', ''),
                client_feedback_quote_fr=pdata.get('quote_fr', ''),
                client_feedback_quote_ar=pdata.get('quote_ar', ''),
                client_feedback_author=pdata.get('quote_author', ''),
                client_feedback_role=pdata.get('quote_role', ''),
                is_featured=pdata['feat'],
                order=pdata['order'],
            )
            if img:
                p.image.save(f'{seed}.jpg', img, save=False)
            p.save()
            created_projects += 1

            # Seed 2 gallery images for the project carousel
            gimg1 = get_image_file('projects', f'{seed}_gallery1', f'{seed}_gallery1.jpg', f'https://picsum.photos/seed/{seed}1/800/500')
            if gimg1:
                pi1 = ProjectImage(
                    project=p,
                    caption_en=f"{pdata['title_en']} — Interface Architecture",
                    caption_fr=f"{pdata['title_fr']} — Architecture de l'interface",
                    caption_ar=f"{pdata['title_ar']} — معمارية الواجهة الرقمية",
                    order=1,
                )
                pi1.image.save(f'{seed}_gallery1.jpg', gimg1, save=True)

            gimg2 = get_image_file('projects', f'{seed}_gallery2', f'{seed}_gallery2.jpg', f'https://picsum.photos/seed/{seed}2/800/500')
            if gimg2:
                pi2 = ProjectImage(
                    project=p,
                    caption_en=f"{pdata['title_en']} — Performance Metrics & Dashboard",
                    caption_fr=f"{pdata['title_fr']} — Métriques & Tableau de bord",
                    caption_ar=f"{pdata['title_ar']} — مؤشرات الأداء ولوحة التحكم",
                    order=2,
                )
                pi2.image.save(f'{seed}_gallery2.jpg', gimg2, save=True)

        self.stdout.write(f'  [OK] Created {created_projects} detailed multilingual projects with gallery carousels')


        # ── 6. Team Members ──
        TeamMember.objects.all().delete()
        team_data = [
            (
                'Ayyoub Beroigui',
                'Founder',
                'Fondateur',
                'المؤسس',
                'Visionary technologist and founder driving high-velocity software engineering, scalable architectures, and digital transformation.',
                'Technologue visionnaire et fondateur pilotant l\'ingénierie logicielle haute performance, les architectures évolutives et la transformation digitale.',
                'مبتكر تقني ومؤسس يقود مسيرة هندسة البرمجيات عالية الأداء والمعماريات السحابية القابلة للتوسع والتحول الرقمي.',
                'ayyoub', 1,
            ),
            (
                'Simo Darkaoui',
                'Developer',
                'Développeur',
                'مطور برمجيات',
                'Full-stack software developer focused on robust web applications, scalable backend systems, and clean modern architecture.',
                'Développeur full-stack spécialisé dans les applications web robustes, les systèmes backend évolutifs et l\'architecture moderne.',
                'مطور برمجيات متكامل يركز على بناء تطبيقات ويب متطورة وأنظمة خلفية قابلة للتوسع وهندسة برمجية عالية الجودة.',
                'simo', 2,
            ),
            (
                'Rajae Belhaj',
                'Commercial & Business Development',
                'Responsable Commerciale',
                'المسؤولة التجارية وتطوير الأعمال',
                'Driving client relationships, strategic accounts, and tailored software partnerships for businesses and enterprise clients.',
                'Développement des partenariats stratégiques, relation client et accompagnement commercial pour les solutions d\'entreprise.',
                'إدارة علاقات العملاء والشراكات الاستراتيجية وتقديم حلول برمجية مخصصة للشركات والمؤسسات.',
                'rajae', 3,
            ),
        ]
        created_team = 0
        for name, r_en, r_fr, r_ar, b_en, b_fr, b_ar, seed, order in team_data:
            photo = get_image_file('team', seed, f'{seed}.jpg', f'https://picsum.photos/seed/{seed}/300/300')
            tm = TeamMember(
                name=name, role_en=r_en, role_fr=r_fr, role_ar=r_ar,
                bio_en=b_en, bio_fr=b_fr, bio_ar=b_ar,
                order=order,
            )
            if photo:
                tm.photo.save(f'{seed}.jpg', photo, save=False)
            tm.save()
            created_team += 1
        self.stdout.write(f'  [OK] Created {created_team} multilingual team members')

        # ── 7. Testimonials ──
        Testimonial.objects.all().delete()
        testimonials_data = [
            (
                'Ahmed Benkirane',
                'Chief Technology Officer',
                'Directeur Technique (CTO)',
                'المدير التقني',
                'Atlas Capital',
                'getNexiro delivered a mission-critical platform that transformed our digital operations. Their technical depth and responsiveness are unmatched.',
                'getNexiro a livré une plateforme stratégique qui a transformé nos opérations. Leur rigueur technique et réactivité sont incomparables.',
                'قدمت لنا getNexiro منصة حيوية أعادت تشكيل عملياتنا الرقمية بالكامل. عمقهم الهندسي وسرعة استجابتهم لا مثيل لها.',
                'ahmed', 1,
            ),
            (
                'Claire Dubois',
                'VP of Digital Transformation',
                'Vice-Présidente Transformation Digitale',
                'نائبة رئيس التحول الرقمي',
                'EuroMed Freight',
                'Working with the getNexiro team in Tangier gave us European-caliber software engineering with seamless timezone alignment and outstanding ROI.',
                'Collaborer avec getNexiro à Tanger nous a apporté une qualité logicielle européenne avec un alignement horaire idéal et un ROI exceptionnel.',
                'العمل مع فريق getNexiro في طنجة منحنا هندسة برمجيات بمعايير أوروبية وتوافق زمني ممتاز وعائداً استثنائياً على الاستثمار.',
                'claire', 2,
            ),
            (
                'Dr. Omar Fassi',
                'Co-Founder & CEO',
                'Cofondateur & PDG',
                'المؤسس المشارك والرئيس التنفيذي',
                'MedConnect Health',
                'From system architecture to final deployment, getNexiro demonstrated extraordinary craftsmanship and deep healthcare domain expertise.',
                'De l\'architecture au déploiement final, getNexiro a fait preuve d\'un savoir-faire remarquable et d\'une réelle expertise métier.',
                'من تصميم البنية المعمارية إلى الإطلاق النهائي، أثبتت getNexiro براعة استثنائية وفهماً عميقاً لمتطلبات قطاع الرعاية الصحية.',
                'omar', 3,
            ),
        ]
        created_testimonials = 0
        for name, r_en, r_fr, r_ar, company, q_en, q_fr, q_ar, seed, order in testimonials_data:
            avatar = get_image_file('testimonials', seed, f'{seed}.jpg', f'https://picsum.photos/seed/{seed}/100/100')
            t = Testimonial(
                author_name=name, author_role_en=r_en, author_role_fr=r_fr, author_role_ar=r_ar,
                company=company, quote_en=q_en, quote_fr=q_fr, quote_ar=q_ar,
                is_featured=True, order=order,
            )
            if avatar:
                t.avatar.save(f'{seed}.jpg', avatar, save=False)
            t.save()
            created_testimonials += 1
        self.stdout.write(f'  [OK] Created {created_testimonials} multilingual testimonials')

        # ── 8. Client Logos (They Trust Us) ──
        ClientLogo.objects.all().delete()
        clients_data = [
            ('MEDICENTERS PERFORMANCE', 'https://medicentersperformance.com', 'medicenters.png', 1),
            ('CAPERSMED', 'https://capersmed.com', 'capersmed.png', 2),
            ('Laboratoire International', 'https://laboratoiretanger.com', 'laboratoire.png', 3),
            ('Vinaigre du Maroc', 'https://vinaigredumaroc.com', 'vinaigre.png', 4),
        ]
        created_clients = 0
        for name, url, filename, order in clients_data:
            logo_file = get_image_file('clients', filename.split('.')[0], filename, f'https://picsum.photos/seed/{filename.split(".")[0]}/200/80')
            cl = ClientLogo(name=name, url=url, order=order)
            if logo_file:
                cl.logo.save(filename, logo_file, save=False)
            cl.save()
            created_clients += 1
        self.stdout.write(f'  [OK] Created {created_clients} client logos')

        # ── 9. Company Values (About Page) ──
        CompanyValue.objects.all().delete()
        company_values_data = [
            (
                '🌍',
                'Gateway Location',
                'Emplacement Stratégique',
                'موقع استراتيجي وبوابة القارات',
                'Just 14 km from Europe, Tangier offers GMT+1 timezone alignment with European clients and easy travel to major business hubs.',
                'À seulement 14 km de l\'Europe, Tanger offre un alignement sur le fuseau GMT+1 avec nos clients européens et un accès rapide aux pôles économiques majeurs.',
                'على بعد 14 كم فقط من أوروبا، توفر طنجة توافقاً كاملاً مع التوقيت الأوروبي (GMT+1) وسهولة الوصول إلى كبرى العواصم الاقتصادية.',
                1,
            ),
            (
                '💡',
                'Rich Talent Pool',
                'Vivier de Talents Exceptionnel',
                'كفاءات وخبرات هندسية رائدة',
                "Morocco's growing tech ecosystem provides access to multilingual, highly skilled engineers and designers.",
                "L'écosystème technologique en plein essor au Maroc nous permet de réunir des ingénieurs et designers multilingues hautement qualifiés.",
                'يوفر النظام التكنولوجي الصاعد في المغرب نخبة من المهندسين والمصممين متعددي اللغات والمهارات العالمية الفائقة.',
                2,
            ),
            (
                '💎',
                'Premium Value',
                'Valeur & Excellence',
                'قيمة استثنائية وأعلى عائد استثماري',
                'World-class quality at competitive rates — delivering exceptional ROI without compromising on craftsmanship.',
                'Une qualité de niveau mondial à des tarifs compétitifs — offrant un retour sur investissement exceptionnel sans compromis technique.',
                'جودة عالمية بأسعار تنافسية تحقق أقصى عائد على الاستثمار دون أي مساومة على معايير الإتقان والدقة.',
                3,
            ),
        ]
        created_values = 0
        for icon, t_en, t_fr, t_ar, d_en, d_fr, d_ar, order in company_values_data:
            CompanyValue.objects.create(
                icon=icon,
                title_en=t_en, title_fr=t_fr, title_ar=t_ar,
                description_en=d_en, description_fr=d_fr, description_ar=d_ar,
                order=order,
            )
            created_values += 1
        self.stdout.write(f'  [OK] Created {created_values} company values')

        # ── 10. Process Steps (Services Page) ──
        ProcessStep.objects.all().delete()
        process_steps_data = [
            (
                '01',
                'Discovery',
                'Découverte',
                'الاستكشاف والتحليل',
                'We deep-dive into your business requirements, user needs, and technical landscape.',
                'Nous analysons en profondeur vos besoins métier, les attentes utilisateurs et votre environnement technologique.',
                'نتعمق في متطلبات عملك واحتياجات المستخدمين والبنية التقنية الحالية لبناء أساس متين.',
                'Requirements, Research',
                1,
            ),
            (
                '02',
                'Architecture',
                'Architecture',
                'التصميم والهندسة',
                'We design scalable system architectures and create detailed technical specifications.',
                'Nous concevons des architectures évolutives et rédigeons des spécifications techniques rigoureuses.',
                'نصمم معمارية أنظمة مرنة وقابلة للتوسع ونضع المواصفات الفنية التفصيلية.',
                'Design, Planning',
                2,
            ),
            (
                '03',
                'Development',
                'Développement',
                'التطوير البرمجي',
                'Agile sprints with continuous integration, automated testing, and frequent deliverables.',
                'Sprints agiles avec intégration continue, tests automatisés et livrables fréquents.',
                'سبرنتات مرنة (Agile) مع تكامل مستمر واختبارات مؤتمتة وتسليمات مرحلية منتظمة.',
                'Agile, CI/CD',
                3,
            ),
            (
                '04',
                'Launch & Support',
                'Lancement & Support',
                'الإطلاق والدعم المستمر',
                'Production deployment, performance monitoring, and ongoing maintenance partnerships.',
                'Mise en production sécurisée, surveillance des performances et partenariat de maintenance continue.',
                'نشر آمن في بيئة الإنتاج، مراقبة فورية للأداء، وشراكة دعم وصيانة متواصلة.',
                'Deploy, Monitor',
                4,
            ),
        ]
        created_steps = 0
        for num, t_en, t_fr, t_ar, d_en, d_fr, d_ar, tags, order in process_steps_data:
            ProcessStep.objects.create(
                step_number=num,
                title_en=t_en, title_fr=t_fr, title_ar=t_ar,
                description_en=d_en, description_fr=d_fr, description_ar=d_ar,
                tags=tags,
                order=order,
            )
            created_steps += 1
        self.stdout.write(f'  [OK] Created {created_steps} process steps')

        # ── 11. Store Items (Store Page) ──
        StoreItem.objects.all().delete()
        store_items_data = [
            (
                '🎨',
                'Design Systems',
                'Design Systems',
                'أنظمة التصميم UI/UX',
                'Production-ready UI kits and component libraries.',
                'Kits UI prêts pour la production et bibliothèques de composants.',
                'حزم واجهات مستخدم جاهزة للإنتاج ومكتبات عناصر بصرية متكاملة.',
                'COMING SOON', 'BIENTÔT DISPONIBLE', 'قريباً',
                1, True,
            ),
            (
                '⚡',
                'Starter Templates',
                'Modèles de Démarrage',
                'قوالب انطلاق للمشاريع',
                'Django & React project boilerplates with best practices.',
                'Boilerplates de projets Django & React intégrant les meilleures pratiques.',
                'قوالب هيكلية متقدمة لمشاريع Django و React بأعلى المعايير الهندسية.',
                'COMING SOON', 'BIENTÔT DISPONIBLE', 'قريباً',
                2, True,
            ),
            (
                '🛠️',
                'Dev Tools',
                'Outils Développeurs',
                'أدوات المطورين والأتمتة',
                'CLI tools, scripts, and automation utilities.',
                'Outils CLI, scripts et utilitaires d\'automatisation performants.',
                'أدوات سطر الأوامر، سكربتات وحلول أتمتة لرفع الإنتاجية والتطوير.',
                'COMING SOON', 'BIENTÔT DISPONIBLE', 'قريباً',
                3, True,
            ),
        ]
        created_store_items = 0
        for emoji, t_en, t_fr, t_ar, d_en, d_fr, d_ar, b_en, b_fr, b_ar, order, is_active in store_items_data:
            StoreItem.objects.create(
                emoji=emoji,
                title_en=t_en, title_fr=t_fr, title_ar=t_ar,
                description_en=d_en, description_fr=d_fr, description_ar=d_ar,
                badge_en=b_en, badge_fr=b_fr, badge_ar=b_ar,
                order=order,
                is_active=is_active,
            )
            created_store_items += 1
        self.stdout.write(f'  [OK] Created {created_store_items} store preview items')

        # ── 12. Blog Categories & Posts ──
        BlogCategory.objects.all().delete()
        BlogPost.objects.all().delete()

        blog_cats = {
            'engineering': BlogCategory.objects.create(
                name_en='Engineering', name_fr='Ingénierie', name_ar='الهندسة', slug='engineering',
            ),
            'design': BlogCategory.objects.create(
                name_en='Design', name_fr='Design', name_ar='التصميم', slug='design',
            ),
            'business': BlogCategory.objects.create(
                name_en='Business & Strategy', name_fr='Business & Stratégie', name_ar='الأعمال والاستراتيجية', slug='business-strategy',
            ),
        }

        from django.utils import timezone
        now = timezone.now()

        blog_posts = [
            {
                'title_en': 'Why Django is the Best Framework for Enterprise Web Applications in 2026',
                'title_fr': 'Pourquoi Django est le meilleur framework pour les applications web d\'entreprise en 2026',
                'title_ar': 'لماذا يعد Django أفضل إطار عمل لتطبيقات الويب المؤسسية في 2026',
                'slug': 'django-best-framework-enterprise-web-2026',
                'excerpt_en': 'Discover why leading enterprises choose Django for building scalable, secure, and maintainable web applications. From rapid development to built-in security, explore the key advantages.',
                'excerpt_fr': 'Découvrez pourquoi les grandes entreprises choisissent Django pour construire des applications web évolutives, sécurisées et maintenables.',
                'excerpt_ar': 'اكتشف لماذا تختار المؤسسات الكبرى Django لبناء تطبيقات ويب قابلة للتوسع وآمنة وسهلة الصيانة.',
                'body_en': '''<h2>The Enterprise Framework of Choice</h2>
<p>In the ever-evolving landscape of web development, Django continues to stand out as the go-to framework for enterprise-grade applications. Companies like Instagram, Mozilla, and NASA trust Django for their mission-critical systems — and for good reason.</p>

<h2>1. Batteries-Included Philosophy</h2>
<p>Django ships with everything you need out of the box: an ORM, authentication system, admin dashboard, form handling, and more. This <strong>"batteries-included"</strong> approach means your team spends less time integrating third-party libraries and more time building business logic.</p>

<h3>Built-in Admin Dashboard</h3>
<p>One of Django's most powerful features is its auto-generated admin interface. With just a few lines of code, you get a fully functional content management system that non-technical team members can use immediately.</p>

<h2>2. Security First</h2>
<p>Django was designed with security as a priority. It provides built-in protection against:</p>
<ul>
<li><strong>SQL Injection</strong> — through its ORM and parameterized queries</li>
<li><strong>Cross-Site Scripting (XSS)</strong> — automatic HTML escaping in templates</li>
<li><strong>Cross-Site Request Forgery (CSRF)</strong> — built-in CSRF middleware</li>
<li><strong>Clickjacking</strong> — X-Frame-Options middleware</li>
</ul>

<h2>3. Scalability That Grows With You</h2>
<p>Django's architecture supports horizontal scaling through database routing, caching frameworks (Redis, Memcached), and async views introduced in Django 4.1+. Whether you're serving thousands or millions of users, Django can handle it.</p>

<blockquote>Django's ORM makes database operations intuitive, while its migration system ensures schema changes are safe and reversible across distributed teams.</blockquote>

<h2>4. Rich Ecosystem & Community</h2>
<p>With over 80,000 packages on PyPI and one of the most active open-source communities, finding solutions and getting help is never a problem. Django REST Framework, Celery, and django-allauth are just a few of the battle-tested packages available.</p>

<h2>Why getNexiro Builds With Django</h2>
<p>At getNexiro, we've built dozens of enterprise applications using Django. Its combination of rapid development, security, and scalability makes it our framework of choice for clients who need reliable, production-grade solutions.</p>

<p>Ready to build your next web application? <a href="/en/contact/">Get in touch with our team</a> for a free consultation.</p>''',
                'body_fr': '''<h2>Le framework de choix pour l'entreprise</h2>
<p>Dans le paysage en constante évolution du développement web, Django continue de se démarquer comme le framework incontournable pour les applications de niveau entreprise.</p>

<h2>1. Philosophie "Batteries Incluses"</h2>
<p>Django est livré avec tout ce dont vous avez besoin : un ORM, un système d'authentification, un tableau de bord admin, la gestion des formulaires et bien plus.</p>

<h2>2. Sécurité d'abord</h2>
<p>Django a été conçu avec la sécurité comme priorité, offrant une protection intégrée contre les injections SQL, XSS, CSRF et le clickjacking.</p>

<h2>3. Évolutivité</h2>
<p>L'architecture de Django supporte la mise à l'échelle horizontale grâce au routage de base de données, aux frameworks de cache et aux vues asynchrones.</p>

<h2>Pourquoi getNexiro utilise Django</h2>
<p>Chez getNexiro, nous avons construit des dizaines d'applications d'entreprise avec Django. Sa combinaison de développement rapide, de sécurité et d'évolutivité en fait notre choix de prédilection.</p>''',
                'body_ar': '''<h2>إطار العمل المفضل للمؤسسات</h2>
<p>في المشهد المتطور باستمرار لتطوير الويب، يستمر Django في التميز كإطار العمل المفضل للتطبيقات على مستوى المؤسسات.</p>

<h2>1. فلسفة "البطاريات مضمنة"</h2>
<p>يأتي Django مع كل ما تحتاجه: ORM ونظام مصادقة ولوحة إدارة ومعالجة نماذج والمزيد.</p>

<h2>2. الأمان أولاً</h2>
<p>تم تصميم Django مع الأمان كأولوية، حيث يوفر حماية مدمجة ضد حقن SQL وXSS وCSRF والنقر الخادع.</p>

<h2>لماذا تبني getNexiro باستخدام Django</h2>
<p>في getNexiro، قمنا ببناء عشرات التطبيقات المؤسسية باستخدام Django. مزيجه من التطوير السريع والأمان وقابلية التوسع يجعله خيارنا المفضل.</p>''',
                'meta_title_en': 'Why Django is Best for Enterprise Web Apps in 2026',
                'meta_title_fr': 'Pourquoi Django est le meilleur pour les apps web entreprise en 2026',
                'meta_title_ar': 'لماذا Django الأفضل لتطبيقات الويب المؤسسية 2026',
                'meta_description_en': 'Learn why Django remains the top choice for enterprise web development in 2026. Security, scalability, and rapid development explained.',
                'meta_description_fr': 'Découvrez pourquoi Django reste le choix numéro un pour le développement web entreprise en 2026.',
                'meta_description_ar': 'تعرف لماذا يظل Django الخيار الأول لتطوير تطبيقات الويب المؤسسية في 2026.',
                'meta_keywords': 'Django, enterprise web development, Python framework, web application, scalability, security, getNexiro, Tangier',
                'category': blog_cats['engineering'],
                'author_name': 'getNexiro Team',
                'reading_time_minutes': 7,
                'tags': 'Django, Python, Web Development, Enterprise, Backend',
                'status': 'published',
                'is_featured': True,
                'published_at': now,
            },
            {
                'title_en': '10 UI/UX Design Principles That Convert Visitors Into Customers',
                'title_fr': '10 principes de design UI/UX qui convertissent les visiteurs en clients',
                'title_ar': '10 مبادئ تصميم UI/UX تحول الزوار إلى عملاء',
                'slug': 'ui-ux-design-principles-convert-visitors-customers',
                'excerpt_en': 'Master the design principles that leading agencies use to create high-converting digital experiences. From visual hierarchy to micro-interactions, here\'s what actually works.',
                'excerpt_fr': 'Maîtrisez les principes de design que les agences leaders utilisent pour créer des expériences digitales à forte conversion.',
                'excerpt_ar': 'أتقن مبادئ التصميم التي تستخدمها الوكالات الرائدة لإنشاء تجارب رقمية عالية التحويل.',
                'body_en': '''<h2>Design That Drives Results</h2>
<p>Great design isn't just about aesthetics — it's about creating experiences that guide users toward meaningful actions. After years of building digital products, we've distilled the most impactful UI/UX principles that consistently drive conversions.</p>

<h2>1. Visual Hierarchy is Everything</h2>
<p>Users should instantly understand what's most important on your page. Use size, color, contrast, and whitespace to create a clear hierarchy that guides the eye naturally.</p>

<h2>2. The 3-Second Rule</h2>
<p>You have approximately 3 seconds to communicate your value proposition. Your hero section must answer three questions: <strong>What do you do? Who is it for? Why should I care?</strong></p>

<h2>3. Reduce Cognitive Load</h2>
<p>Every decision you ask a user to make is friction. Simplify navigation, limit choices (Hick's Law), and use progressive disclosure to reveal complexity only when needed.</p>

<h2>4. Strategic Use of Color</h2>
<p>Color psychology plays a crucial role in conversion. Use your primary action color consistently for CTAs, and ensure sufficient contrast ratios (WCAG 2.1 AA minimum).</p>

<h2>5. Mobile-First Design</h2>
<p>With over 60% of web traffic coming from mobile devices, designing for mobile first ensures your most constrained experience is optimized before scaling up.</p>

<h2>6. Micro-Interactions Build Trust</h2>
<p>Subtle animations on button hovers, form submissions, and page transitions create a polished experience that builds unconscious trust with your users.</p>

<h2>7. Social Proof Placement</h2>
<p>Place testimonials, client logos, and case study results near your CTAs. Social proof reduces uncertainty at the exact moment users are making a decision.</p>

<h2>8. F-Pattern & Z-Pattern Layouts</h2>
<p>Eye-tracking studies show users scan pages in F or Z patterns. Align your most important content with these natural scanning behaviors.</p>

<h2>9. Performance IS UX</h2>
<p>A 1-second delay in page load time can reduce conversions by 7%. Optimize images, minimize HTTP requests, and leverage CDN caching.</p>

<h2>10. Continuous Testing</h2>
<p>The best-performing designs are never guessed — they're tested. Implement A/B testing, heatmaps, and session recordings to make data-driven design decisions.</p>

<h2>Apply These Principles Today</h2>
<p>At getNexiro, we integrate these principles into every project we deliver. Whether you need a complete redesign or a conversion optimization audit, <a href="/en/contact/">let's talk</a>.</p>''',
                'body_fr': '''<h2>Un design qui génère des résultats</h2>
<p>Le bon design n'est pas seulement une question d'esthétique — c'est créer des expériences qui guident les utilisateurs vers des actions significatives.</p>

<h2>1. La hiérarchie visuelle est primordiale</h2>
<p>Les utilisateurs doivent comprendre instantanément ce qui est le plus important sur votre page.</p>

<h2>2. La règle des 3 secondes</h2>
<p>Vous avez environ 3 secondes pour communiquer votre proposition de valeur.</p>

<h2>Appliquez ces principes dès aujourd'hui</h2>
<p>Chez getNexiro, nous intégrons ces principes dans chaque projet que nous livrons.</p>''',
                'body_ar': '''<h2>تصميم يحقق النتائج</h2>
<p>التصميم الجيد ليس مجرد جماليات — إنه إنشاء تجارب توجه المستخدمين نحو إجراءات ذات معنى.</p>

<h2>1. التسلسل البصري هو كل شيء</h2>
<p>يجب أن يفهم المستخدمون على الفور ما هو الأهم في صفحتك.</p>

<h2>2. قاعدة الـ 3 ثوانٍ</h2>
<p>لديك حوالي 3 ثوانٍ لتوصيل عرض القيمة الخاص بك.</p>

<h2>طبق هذه المبادئ اليوم</h2>
<p>في getNexiro، ندمج هذه المبادئ في كل مشروع نقدمه.</p>''',
                'meta_title_en': '10 UI/UX Design Principles That Convert | getNexiro',
                'meta_title_fr': '10 principes UI/UX qui convertissent | getNexiro',
                'meta_title_ar': '10 مبادئ تصميم UI/UX تحول الزوار لعملاء',
                'meta_description_en': 'Discover 10 proven UI/UX design principles that convert website visitors into paying customers. Expert tips from getNexiro design team.',
                'meta_description_fr': 'Découvrez 10 principes de design UI/UX éprouvés qui convertissent les visiteurs en clients payants.',
                'meta_description_ar': 'اكتشف 10 مبادئ تصميم UI/UX مثبتة تحول زوار الموقع إلى عملاء يدفعون.',
                'meta_keywords': 'UI/UX design, conversion optimization, web design principles, user experience, visual hierarchy, getNexiro',
                'category': blog_cats['design'],
                'author_name': 'getNexiro Team',
                'reading_time_minutes': 9,
                'tags': 'UI/UX, Design, Conversion, Web Design, User Experience',
                'status': 'published',
                'is_featured': True,
                'published_at': now - timezone.timedelta(days=3),
            },
            {
                'title_en': 'How to Choose the Right Tech Stack for Your Startup in Morocco',
                'title_fr': 'Comment choisir la bonne stack technique pour votre startup au Maroc',
                'title_ar': 'كيف تختار المجموعة التقنية المناسبة لشركتك الناشئة في المغرب',
                'slug': 'choose-right-tech-stack-startup-morocco',
                'excerpt_en': 'Choosing the right technology stack can make or break your startup. Here\'s a practical guide for Moroccan entrepreneurs on selecting technologies that balance speed, cost, and scalability.',
                'excerpt_fr': 'Choisir la bonne stack technique peut faire ou défaire votre startup. Guide pratique pour les entrepreneurs marocains.',
                'excerpt_ar': 'اختيار المجموعة التقنية المناسبة يمكن أن يصنع أو يدمر شركتك الناشئة. دليل عملي لرواد الأعمال المغاربة.',
                'body_en': '''<h2>The Technology Decision That Shapes Your Future</h2>
<p>For startups in Morocco's growing tech ecosystem — from Casablanca to Tangier — choosing the right tech stack is one of the most consequential decisions you'll make. The wrong choice can lead to expensive rewrites, slow development, and difficulty hiring talent.</p>

<h2>Understanding Your Requirements First</h2>
<p>Before looking at specific technologies, answer these critical questions:</p>
<ul>
<li><strong>Time to market:</strong> How quickly do you need to launch your MVP?</li>
<li><strong>Scale expectations:</strong> Will you serve hundreds or millions of users?</li>
<li><strong>Team availability:</strong> What talent pool exists in your region?</li>
<li><strong>Budget constraints:</strong> What's your runway for development?</li>
</ul>

<h2>Recommended Stacks by Use Case</h2>

<h3>For Web Applications: Django + React</h3>
<p>This combination offers rapid backend development with Django's batteries-included approach, paired with React's component-based frontend architecture. It's our most recommended stack for B2B SaaS products.</p>

<h3>For Mobile Apps: Flutter</h3>
<p>Flutter provides a single codebase for iOS and Android with native performance. For startups watching their budget, it eliminates the need for two separate development teams.</p>

<h3>For E-Commerce: Django + Next.js</h3>
<p>Server-side rendering with Next.js provides the SEO benefits e-commerce sites need, while Django handles complex business logic, inventory, and payment processing.</p>

<h2>The Morocco Factor</h2>
<p>When building a startup in Morocco, consider the local developer ecosystem. Python/Django and JavaScript developers are abundant in cities like Casablanca, Rabat, and Tangier, making hiring easier and more cost-effective.</p>

<blockquote>The best tech stack is the one your team can build, maintain, and scale with confidence.</blockquote>

<h2>Need Help Deciding?</h2>
<p>At getNexiro, we offer free technical consultations to help startups choose the right technologies. <a href="/en/contact/">Schedule a call</a> with our engineering team today.</p>''',
                'body_fr': '''<h2>La décision technologique qui façonne votre avenir</h2>
<p>Pour les startups dans l'écosystème tech croissant du Maroc, choisir la bonne stack technique est l'une des décisions les plus importantes.</p>

<h2>Comprendre vos besoins d'abord</h2>
<p>Avant de regarder des technologies spécifiques, répondez à ces questions critiques sur le temps de mise en marché, les attentes d'échelle, la disponibilité des talents et les contraintes budgétaires.</p>

<h2>Stacks recommandées par cas d'utilisation</h2>
<p>Pour les applications web: Django + React. Pour les apps mobiles: Flutter. Pour le e-commerce: Django + Next.js.</p>

<h2>Besoin d'aide pour décider ?</h2>
<p>Chez getNexiro, nous offrons des consultations techniques gratuites pour aider les startups à choisir les bonnes technologies.</p>''',
                'body_ar': '''<h2>القرار التقني الذي يشكل مستقبلك</h2>
<p>بالنسبة للشركات الناشئة في النظام البيئي التقني المتنامي في المغرب، يعد اختيار المجموعة التقنية المناسبة من أهم القرارات.</p>

<h2>فهم متطلباتك أولاً</h2>
<p>قبل النظر في تقنيات محددة، أجب على هذه الأسئلة الحرجة حول وقت الوصول للسوق وتوقعات النطاق وتوفر الفريق وقيود الميزانية.</p>

<h2>المجموعات الموصى بها حسب حالة الاستخدام</h2>
<p>لتطبيقات الويب: Django + React. لتطبيقات الجوال: Flutter. للتجارة الإلكترونية: Django + Next.js.</p>

<h2>هل تحتاج مساعدة في القرار؟</h2>
<p>في getNexiro، نقدم استشارات تقنية مجانية لمساعدة الشركات الناشئة على اختيار التقنيات المناسبة.</p>''',
                'meta_title_en': 'Choosing the Right Tech Stack for Your Moroccan Startup',
                'meta_title_fr': 'Choisir la bonne stack tech pour votre startup marocaine',
                'meta_title_ar': 'اختيار المجموعة التقنية لشركتك الناشئة المغربية',
                'meta_description_en': 'Practical guide for Moroccan startups on choosing the best tech stack. Django, React, Flutter compared for speed, cost, and scalability.',
                'meta_description_fr': 'Guide pratique pour les startups marocaines sur le choix de la meilleure stack technique.',
                'meta_description_ar': 'دليل عملي للشركات الناشئة المغربية حول اختيار أفضل مجموعة تقنية.',
                'meta_keywords': 'tech stack, startup Morocco, Django, React, Flutter, web development Tangier, mobile app Morocco, getNexiro',
                'category': blog_cats['business'],
                'author_name': 'getNexiro Team',
                'reading_time_minutes': 6,
                'tags': 'Startup, Morocco, Tech Stack, Django, React, Flutter, Strategy',
                'status': 'published',
                'is_featured': False,
                'published_at': now - timezone.timedelta(days=7),
            },
        ]
        for post_data in blog_posts:
            BlogPost.objects.create(**post_data)
        self.stdout.write(f'  [OK] Created {len(blog_cats)} blog categories and {len(blog_posts)} SEO-optimized blog posts')

        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Database seeded with 100% complete multilingual content!'))
