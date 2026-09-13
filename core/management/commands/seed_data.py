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
    SiteConfig, Service, ProjectCategory, Project,
    TeamMember, Testimonial, ClientLogo, Stat,
    CompanyValue, ProcessStep, StoreItem,
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
        services_data = [
            (
                'Web Development',
                'Développement Web',
                'تطوير مواقع وتطبيقات الويب',
                'From responsive marketing sites to complex SaaS platforms, we architect and build robust web solutions using Django, React, and modern cloud stacks.',
                'Des sites vitrines réactifs aux plateformes SaaS complexes, nous concevons et bâtissons des solutions web robustes avec Django, React et les stacks cloud modernes.',
                'من المواقع التعريفية التفاعلية إلى منصات SaaS السحابية المعقدة، نصمم ونطور حلول ويب فائقة الأداء باستخدام Django و React وأحدث التقنيات.',
                'icon-web', True, 1,
            ),
            (
                'Mobile Applications',
                'Applications Mobiles',
                'تطوير تطبيقات الجوال',
                'Native iOS/Android and cross-platform apps built with Flutter and React Native, delivering seamless performance and intuitive user interfaces.',
                'Applications natives iOS/Android et multiplateformes avec Flutter et React Native, offrant une fluidité parfaite et une ergonomie intuitive.',
                'تطبيقات أصلية لنظامي iOS و Android وتطبيقات هجينة عبر Flutter و React Native، بأداء سلس وتصميم واجهات مستخدم جذاب.',
                'icon-mobile', True, 2,
            ),
            (
                'UI/UX & Design Systems',
                'UI/UX & Design Systems',
                'تصميم تجربة وواجهة المستخدم',
                'User research, wireframing, interactive prototyping, and pixel-perfect design systems that elevate your brand and maximize conversion.',
                'Recherche utilisateur, prototypage interactif et design systems au pixel près pour sublimer votre marque et maximiser vos conversions.',
                'أبحاث تجربة المستخدم، النماذج التفاعلية، وتصميم أنظمة واجهات متكاملة ترتقي بعلامتك التجارية وتضاعف معدلات التحويل.',
                'icon-design', True, 3,
            ),
            (
                'Technical Consulting',
                'Conseil Technique',
                'الاستشارات التقنية والمعمارية',
                'Architecture reviews, security audits, and strategic technology roadmapping to ensure your digital investments deliver maximum enterprise ROI.',
                'Audits d\'architecture, revues de sécurité et feuilles de route technologiques stratégiques pour rentabiliser vos investissements digitaux.',
                'تدقيق معمارية الأنظمة، مراجعات الأمان والحماية، ووضع خطط تقنية استراتيجية تضمن تحقيق أعلى عائد على استثماراتكم الرقمية.',
                'icon-consulting', False, 4,
            ),
            (
                'API & Microservices',
                'API & Microservices',
                'واجهات البرمجة والخدمات المصغرة',
                'High-throughput RESTful and GraphQL APIs, seamless third-party integrations, and fault-tolerant microservices architecture.',
                'APIs RESTful et GraphQL haute performance, intégrations tierces fluides et architecture microservices résiliente.',
                'واجهات برمجية RESTful و GraphQL عالية الأداء، تكاملات برمجية سلسة وبنية خدمات مصغرة ذات اعتمادية وموثوقية فائقة.',
                'icon-api', False, 5,
            ),
            (
                'Cloud & DevOps',
                'Cloud & DevOps',
                'الحوسبة السحابية و DevOps',
                'Cloud infrastructure on AWS/GCP, automated CI/CD deployment pipelines, containerization with Docker, and 24/7 observability.',
                'Infrastructures cloud sur AWS/GCP, pipelines CI/CD automatisés, conteneurisation Docker et observabilité continue.',
                'بنية تحتية سحابية متطورة على AWS و GCP، أتمتة خطوط النشر CI/CD، حاويات Docker، ومراقبة أداء مستمرة على مدار الساعة.',
                'icon-cloud', False, 6,
            ),
        ]
        for t_en, t_fr, t_ar, d_en, d_fr, d_ar, icon, feat, order in services_data:
            Service.objects.create(
                title_en=t_en, title_fr=t_fr, title_ar=t_ar,
                description_en=d_en, description_fr=d_fr, description_ar=d_ar,
                icon=icon, is_featured=feat, order=order,
            )
        self.stdout.write(f'  [OK] Created {len(services_data)} multilingual services')

        # ── 4. Project Categories ──
        ProjectCategory.objects.all().delete()
        cats_data = [
            ('Agro-Export', 'Agro-Export', 'الصناعات الغذائية والتصدير', 'agroexport'),
            ('HealthTech', 'HealthTech', 'الصحة الرقمية', 'healthtech'),
            ('Medical Lab', 'Laboratoire Médical', 'المختبر الطبي', 'medlab'),
            ('Food Industry', 'Industrie Alimentaire', 'الصناعات الغذائية', 'food'),
            ('E-Commerce', 'E-Commerce', 'التجارة الإلكترونية', 'ecommerce'),
            ('SaaS', 'SaaS', 'البرمجيات السحابية', 'saas'),
        ]
        cat_map = {}
        for n_en, n_fr, n_ar, slug in cats_data:
            c = ProjectCategory.objects.create(name_en=n_en, name_fr=n_fr, name_ar=n_ar, slug=slug)
            cat_map[slug] = c
        self.stdout.write(f'  [OK] Created {len(cats_data)} multilingual categories')

        # ── 5. Projects ──
        Project.objects.all().delete()
        projects_data = [
            (
                'MEDICENTERS PERFORMANCE',
                'MEDICENTERS PERFORMANCE',
                'منصة ميديسنترز بيرفورمانس',
                'healthtech',
                'Medical architecture, space fitting, and turnkey healthcare design platform with interactive 360° virtual tours.',
                'Plateforme d\'aménagement et agencement d\'espaces médicaux professionnels à Tanger avec visites virtuelles 360° immersives.',
                'منصة رائدة في تهيئة وتجهيز المساحات الطبية والعيادات في طنجة مع جولات افتراضية تفاعلية 360 درجة.',
                'medicenters', True, 1, 'MEDICENTERS PERFORMANCE', 'Django, Bootstrap 5, Pannellum 360, i18n',
            ),
            (
                'CAPERSMED Wholesale Export',
                'CAPERSMED Export Agroalimentaire',
                'منصة كابرز ميد للتصدير الدولي',
                'agroexport',
                'Global B2B agro-food export platform featuring multi-market internationalization across 9 languages, technical SEO, and BRC/IFS certification showcases.',
                'Plateforme B2B mondiale d\'exportation agroalimentaire avec internationalisation en 9 langues, SEO technique et mise en avant des certifications BRC/IFS.',
                'منصة تصدير دولية B2B للصناعات الغذائية تدعم 9 لغات عالمية مع تحسين محركات البحث المتقدم واستعراض شهادات الجودة العالمية BRC و IFS.',
                'capersmed', True, 2, 'CAPERSMED SARL', 'Django, Multilingual (9 langs), SEO, Schema.org',
            ),
            (
                'Laboratoire International Tanger',
                'Laboratoire International de Tanger',
                'المختبر الدولي للتحاليل الطبية بطنجة',
                'medlab',
                'Medical laboratory platform with online results portal, appointment booking, multilingual support, and SEO-optimized health blog.',
                'Plateforme de laboratoire d\'analyses médicales avec portail de résultats en ligne, prise de rendez-vous, support multilingue et blog santé optimisé SEO.',
                'منصة مختبر التحاليل الطبية مع بوابة نتائج إلكترونية وحجز مواعيد ودعم متعدد اللغات ومدونة صحية محسّنة لمحركات البحث.',
                'laboratoire', True, 3, 'Laboratoire International', 'Django, Bootstrap 5, i18n (FR/AR), Blog CMS',
            ),
            (
                'Vinaigre du Maroc',
                'Vinaigre du Maroc',
                'خل المغرب للتصدير',
                'food',
                'B2B export platform for premium Moroccan vinegar and condiments with international BRC/IFS/Halal certifications and multilingual product catalog.',
                'Plateforme d\'exportation B2B de vinaigre et condiments premium marocains avec certifications internationales BRC/IFS/Halal et catalogue produits multilingue.',
                'منصة تصدير B2B للخل والتوابل المغربية الفاخرة مع شهادات الجودة الدولية BRC/IFS/حلال وكتالوج منتجات متعدد اللغات.',
                'vinaigre', True, 4, 'Vinaigre du Maroc SARL', 'Django, Bootstrap 5, SEO, Multilingual',
            ),
            (
                'Diwan Atlas — Customs SaaS',
                'Diwan Atlas — Facturation Douane',
                'ديوان أطلس — منصة الفوترة الجمركية',
                'saas',
                'Bespoke SaaS invoicing and regulatory clearance platform engineered for licensed customs brokers and transit agents in Morocco, featuring automated port fee computation, VAT breakdown, and bilingual FR/AR interface.',
                'Plateforme SaaS métier de facturation et de gestion des dossiers douaniers conçue pour les agents en douane et transitaires au Maroc, avec calcul automatisé des débours, TVA douanière et interface bilingue FR/AR.',
                'منصة سحابية متقدمة لفوترة وإدارة الملفات الجمركية مصممة لوكلاء ومعشري الجمارك في المغرب، تتميز باحتساب آلي للرسوم وتتبع الفواتير والامتثال الضريبي بواجهة ثنائية اللغة.',
                'diwanatlas', True, 5, 'Cabinet de Transit & Douane (Confidentiel)', 'Next.js, TypeScript, Tailwind CSS, PostgreSQL',
            ),
        ]
        created_projects = 0
        for t_en, t_fr, t_ar, cat_slug, d_en, d_fr, d_ar, seed, feat, order, client, tech in projects_data:
            cat = cat_map.get(cat_slug)
            img = get_image_file('projects', seed, f'{seed}.jpg', f'https://picsum.photos/seed/{seed}/600/400')
            
            p = Project(
                title_en=t_en, title_fr=t_fr, title_ar=t_ar,
                description_en=d_en, description_fr=d_fr, description_ar=d_ar,
                category=cat, client_name=client, technologies=tech,
                is_featured=feat, order=order,
            )
            if img:
                p.image.save(f'{seed}.jpg', img, save=False)
            p.save()
            created_projects += 1
            
        self.stdout.write(f'  [OK] Created {created_projects} multilingual projects')

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

        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Database seeded with 100% complete multilingual content!'))
