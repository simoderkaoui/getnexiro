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
        config.phone = '+212 663 017 817'

        config.tagline_en = 'Tech & Dev Services'
        config.tagline_fr = 'Services Tech & Dev'
        config.tagline_ar = 'خدمات التكنولوجيا والتطوير'

        config.hero_title_en = 'We Architect High-Velocity Digital Systems'
        config.hero_title_fr = 'Nous Concevons des Systèmes Numériques Haute-Performance'
        config.hero_title_ar = 'نصمم أنظمة رقمية عالية السرعة والأداء'

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
            ('FinTech', 'FinTech', 'التكنولوجيا المالية', 'fintech'),
            ('HealthTech', 'HealthTech', 'الصحة الرقمية', 'healthtech'),
            ('E-Commerce', 'E-Commerce', 'التجارة الإلكترونية', 'ecommerce'),
            ('Logistics', 'Logistique', 'اللوجستيك والنقل', 'logistics'),
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
                'FinFlow Analytics',
                'FinFlow Analytics',
                'منصة FinFlow المالية',
                'fintech',
                'Real-time financial intelligence dashboard processing millions of daily transactions with sub-second latency.',
                'Tableau de bord d\'intelligence financière en temps réel traitant des millions de transactions quotidiennes.',
                'لوحة تحكم ذكية للتحليلات المالية الفورية تعالج ملايين المعاملات يومياً بدقة وزمن استجابة فائق.',
                'finflow', True, 1, 'Atlas Capital', 'Django, React, Redis, PostgreSQL',
            ),
            (
                'MedConnect Health',
                'MedConnect Santé',
                'منصة MedConnect الطبية',
                'healthtech',
                'Comprehensive telemedicine platform connecting patients across Morocco with board-certified medical specialists.',
                'Plateforme de télémédecine reliant les patients du Maroc aux meilleurs spécialistes médicaux certifiés.',
                'منصة طب عن بعد شاملة تربط المرضى بنخبة من الأطباء والاستشاريين المعتمدين في مختلف أنحاء المغرب.',
                'medconnect', True, 2, 'Morocco Health Network', 'Flutter, Python, WebRTC',
            ),
            (
                'ShopLux Luxury Store',
                'ShopLux Boutique Luxe',
                'متجر ShopLux الفاخر',
                'ecommerce',
                'High-conversion omnichannel luxury e-commerce platform with automated logistics and payment integrations.',
                'Plateforme e-commerce de luxe omnicanale à haute conversion avec logistique automatisée et paiements intégrés.',
                'متجر إلكتروني فاخر متعدد القنوات بمعدلات تحويل عالية مع ربط لوجستي وبوابات دفع إلكتروني متكاملة.',
                'shoplux', True, 3, 'Maison Luxe Tangier', 'Next.js, Django REST, Stripe',
            ),
            (
                'LogiTrack Gateway',
                'LogiTrack Logistique',
                'نظام LogiTrack اللوجستي',
                'logistics',
                'End-to-end supply chain tracking platform connecting Tangier Med port with European freight operators.',
                'Plateforme de traçabilité logistique reliant le port Tanger Med aux transporteurs européens.',
                'منصة إدارة وتتبع سلاسل الإمداد اللوجستية تربط ميناء طنجة المتوسط بشركات الشحن الأوروبية.',
                'logitrack', False, 4, 'EuroMed Cargo', 'Python, Docker, Kafka, Leaflet',
            ),
            (
                'CloudMetrics SaaS',
                'CloudMetrics SaaS',
                'منصة CloudMetrics السحابية',
                'saas',
                'Multi-tenant observability platform providing enterprise teams with infrastructure health insights.',
                'Plateforme d\'observabilité multi-tenant offrant aux équipes d\'entreprise une visibilité totale sur leur infrastructure.',
                'منصة سحابية متقدمة متعددة المستأجرين لمراقبة وتحليل كفاءة واستقرار البنية التحتية البرمجية للمؤسسات.',
                'cloudmetrics', False, 5, 'DataCloud Inc', 'Django, Go, ClickHouse',
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
                'Youssef El Amrani',
                'CEO & Technical Founder',
                'Fondateur & Directeur Général',
                'المؤسس والمدير التنفيذي',
                '12+ years building enterprise systems across Europe and North Africa. Passionate about engineering craftsmanship.',
                'Plus de 12 ans d\'expérience dans les systèmes d\'entreprise en Europe et Afrique du Nord.',
                'أكثر من 12 عاماً في بناء الأنظمة المؤسسية بين أوروبا وشمال إفريقيا، شغوف بجودة وحرفية البرمجيات.',
                'youssef', 1,
            ),
            (
                'Amina Benali',
                'Head of Product & Design',
                'Directrice Produit & Design',
                'مديرة المنتجات والتصميم',
                'Specialized in creating world-class UI/UX design systems that convert complex workflows into effortless interfaces.',
                'Spécialisée dans la création de design systems qui transforment les flux complexes en interfaces intuitives.',
                'متخصصة في تصميم أنظمة الواجهات وتجارب المستخدم التي تبسط العمليات المعقدة إلى واجهات انسيابية وجذابة.',
                'amina', 2,
            ),
            (
                'Karim Tazi',
                'Principal Cloud Architect',
                'Architecte Cloud Principal',
                'كبير مهندسي الحوسبة السحابية',
                'AWS-certified solutions architect specializing in microservices, distributed systems, and zero-downtime deployments.',
                'Architecte certifié AWS expert en microservices, systèmes distribués et déploiements sans interruption.',
                'مهندس معتمد من AWS متخصص في الخدمات المصغرة، الأنظمة الموزعة، والنشر السحابي بدون أي انقطاع في الخدمة.',
                'karim', 3,
            ),
            (
                'Sara Idrissi',
                'Lead Full-Stack Engineer',
                'Ingénieure Full-Stack Lead',
                'كبيرة مهندسي البرمجيات Full-Stack',
                'Django and React core enthusiast focused on high-performance backend pipelines and accessible modern web apps.',
                'Experte Django et React dédiée aux architectures backend haute performance et aux applications web accessibles.',
                'خبيرة في أطر عمل Django و React، تركز على بناء خطوط معالجة خلفية فائقة السرعة وتطبيقات ويب عصرية.',
                'sara', 4,
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

        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Database seeded with 100% complete multilingual content!'))
