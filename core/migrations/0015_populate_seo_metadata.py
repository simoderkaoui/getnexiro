from django.db import migrations


def populate_seo_data(apps, schema_editor):
    SiteConfig = apps.get_model('core', 'SiteConfig')
    Service = apps.get_model('core', 'Service')
    Project = apps.get_model('core', 'Project')
    CityServicePage = apps.get_model('core', 'CityServicePage')
    BlogPost = apps.get_model('core', 'BlogPost')

    # 1. SiteConfig
    config = SiteConfig.objects.first()
    if config:
        config.home_seo_title_en = 'Web & App Development Agency in Tangier | getNexiro'
        config.home_seo_title_fr = 'Agence Web à Tanger — Sites & Applications | getNexiro'
        config.home_seo_title_ar = 'وكالة تطوير مواقع وتطبيقات بطنجة | getNexiro'
        config.home_seo_description_en = 'Premier web and mobile app development agency in Tangier, Morocco. We engineer high-performance platforms for SMBs. Request your free quote today.'
        config.home_seo_description_fr = "Agence de développement web et mobile à Tanger au Maroc. Nous concevons des plateformes performantes pour entreprises. Demandez votre devis gratuit dès aujourd'hui."
        config.home_seo_description_ar = 'وكالة رائدة في تطوير مواقع وتطبيقات الجوال بطنجة والمغرب. تصمم منصات رقمية عالية الأداء للشركات. اطلب عرض سعر مجاني لمشروعك الآن.'

        config.about_seo_title_en = 'About Our Software Agency in Tangier | getNexiro'
        config.about_seo_title_fr = 'À Propos de Notre Agence Web à Tanger | getNexiro'
        config.about_seo_title_ar = 'من نحن — وكالة برمجيات في طنجة | getNexiro'
        config.about_seo_description_en = 'Meet getNexiro, a premier software engineering studio in Tangier, Morocco. Discover our team, values, and engineering standards. Contact us to collaborate.'
        config.about_seo_description_fr = "Découvrez getNexiro, studio d'ingénierie logicielle basé à Tanger, Maroc. Explorez notre équipe, nos valeurs et nos méthodes. Contactez-nous pour votre projet."
        config.about_seo_description_ar = 'تعرف على استوديو البرمجيات getNexiro بطنجة، المغرب. اكتشف فريقنا الهندسي وقيمنا في بناء حلول رقمية متميزة. تواصل معنا لمناقشة مشروعك.'

        config.services_seo_title_en = 'Custom Software & Web Services | getNexiro'
        config.services_seo_title_fr = 'Services de Développement Web & Mobile | getNexiro'
        config.services_seo_title_ar = 'خدمات تطوير البرمجيات والويب | getNexiro'
        config.services_seo_description_en = 'Comprehensive web development, mobile apps, UI/UX design, and cloud services in Tangier, Morocco. Scalable solutions. Get a free technical consultation.'
        config.services_seo_description_fr = 'Développement web sur mesure, applications mobiles, design UI/UX et infrastructure cloud à Tanger, Maroc. Solutions scalables. Obtenez une consultation offerte.'
        config.services_seo_description_ar = 'خدمات متكاملة في تطوير الويب، تطبيقات الجوال، تصميم واجهات المستخدم، وحلول السحابة بطنجة والمغرب. اطلب استشارة تقنية مجانية لمشروعك اليوم.'

        config.projects_seo_title_en = 'Software & Web Development Portfolio | getNexiro'
        config.projects_seo_title_fr = 'Nos Réalisations Web & Applications | getNexiro'
        config.projects_seo_title_ar = 'معرض مشاريعنا وتطبيقاتنا | getNexiro'
        config.projects_seo_description_en = 'Explore our verified case studies in web development, SaaS platforms, and enterprise portals across Morocco and Europe. View our results and contact us.'
        config.projects_seo_description_fr = "Explorez nos études de cas vérifiées en développement web, SaaS et plateformes d'entreprise au Maroc et en Europe. Découvrez nos résultats et parlons-en."
        config.projects_seo_description_ar = 'تصفح دراسات الحالة ومشاريع تطوير الويب وتطبيقات المؤسسات في المغرب وأوروبا من إنجاز getNexiro. استكشف النتائج وتواصل معنا لبدء مشروعك.'

        config.blog_seo_title_en = 'Tech & Software Engineering Insights | getNexiro'
        config.blog_seo_title_fr = 'Blog & Actualités Tech et Ingénierie | getNexiro'
        config.blog_seo_title_ar = 'مدونة التكنولوجيا وهندسة البرمجيات | getNexiro'
        config.blog_seo_description_en = 'Practical software engineering tutorials, Django guides, UI/UX principles, and Moroccan tech insights. Read our latest articles and boost your knowledge.'
        config.blog_seo_description_fr = "Tutoriels d'ingénierie logicielle, guides Django, principes UI/UX et analyses de l'écosystème tech marocain. Lisez nos articles et accélérez votre croissance."
        config.blog_seo_description_ar = 'دروس في هندسة البرمجيات، أدلة إطار عمل دجانغو، مبادئ تجربة المستخدم، ومستجدات التكنولوجيا في المغرب. اقرأ أحدث المقالات وشاركنا رأيك.'

        config.contact_seo_title_en = 'Contact Our Studio in Tangier, Morocco | getNexiro'
        config.contact_seo_title_fr = 'Contactez Notre Agence Web à Tanger | getNexiro'
        config.contact_seo_title_ar = 'تواصل معنا — استشارة تقنية بطنجة | getNexiro'
        config.contact_seo_description_en = 'Get in touch with getNexiro in Tangier, Morocco. Schedule a technical discovery call or request a detailed project proposal. We reply within 24 hours.'
        config.contact_seo_description_fr = 'Prenez contact avec getNexiro à Tanger au Maroc. Planifiez un appel de cadrage ou demandez une proposition sur mesure. Réponse garantie sous 24 heures.'
        config.contact_seo_description_ar = 'تواصل مع فريق getNexiro في طنجة، المغرب. احجز جلسة استشارية تقنية أو اطلب دراسة متكاملة لمشروعك. نرد على استفساراتكم خلال أقل من 24 ساعة.'

        config.packages_seo_title_en = 'Transparent Development Packages | getNexiro'
        config.packages_seo_title_fr = 'Packs de Développement Web Transparents | getNexiro'
        config.packages_seo_title_ar = 'باقات تطوير شفافة للشركات | getNexiro'
        config.packages_seo_description_en = 'Clear, fixed-scope development packages for websites, MVP platforms, and mobile apps in Morocco. Transparent pricing with no surprises. Choose your plan.'
        config.packages_seo_description_fr = 'Packs de développement au forfait pour sites web, plateformes MVP et applications mobiles au Maroc. Tarification claire et sans surprise. Choisissez votre pack.'
        config.packages_seo_description_ar = 'باقات تطوير برمجيات محددة النطاق للمواقع وتطبيقات الجوال والمنصات الناشئة بالمغرب. تسعير واضح وبدون مفاجآت. اختر الباقة المناسبة لمشروعك الآن.'

        config.save()

    # 2. Services
    service_metadata = {
        'web-development': {
            'title_en': 'Web Development in Tangier, Morocco | getNexiro',
            'title_fr': 'Développement Web à Tanger, Maroc | getNexiro',
            'title_ar': 'تطوير المواقع في طنجة، المغرب | getNexiro',
            'desc_en': 'High-performance custom web development in Tangier, Morocco. We engineer responsive, secure Django web platforms for businesses. Get your quote today.',
            'desc_fr': 'Développement web sur mesure à Tanger, Maroc. Nous concevons des sites et plateformes Django rapides, sécurisés et évolutifs. Demandez votre devis gratuit.',
            'desc_ar': 'تطوير مواقع ويب مخصصة وعالية الأداء بطنجة والمغرب. نبني منصات سريعة وآمنة وقابلة للتطوير لدعم نمو أعمالك. اطلب عرض سعر مجاني اليوم.',
        },
        'mobile-applications': {
            'title_en': 'Mobile Applications in Tangier, Morocco | getNexiro',
            'title_fr': 'Applications Mobiles à Tanger, Maroc | getNexiro',
            'title_ar': 'تطبيقات الجوال في طنجة، المغرب | getNexiro',
            'desc_en': 'Native & cross-platform iOS and Android mobile app development in Tangier, Morocco. Intuitive UI, offline sync, fast performance. Book a free call now.',
            'desc_fr': "Création d'applications mobiles iOS et Android à Tanger, Maroc. Interfaces intuitives, synchronisation hors ligne et fluidité. Réservez votre consultation.",
            'desc_ar': 'تطوير تطبيقات الجوال لنظامي iOS وأندرويد بطنجة والمغرب. واجهات استخدام سلسة، أداء سريع ومزامنة متقدمة. احجز مكالمة استشارية مجانية الآن.',
        },
        'uiux-design-systems': {
            'title_en': 'UI/UX Design in Tangier, Morocco | getNexiro',
            'title_fr': 'Design UI/UX à Tanger, Maroc | getNexiro',
            'title_ar': 'تصميم واجهات المستخدم بطنجة | getNexiro',
            'desc_en': 'User research, interactive wireframing, high-fidelity prototypes, and design systems crafted in Tangier, Morocco. Transform your UX. Contact our team.',
            'desc_fr': 'Recherche utilisateur, wireframes interactifs, prototypes haute fidélité et design systems à Tanger, Maroc. Sublimez votre UX. Contactez nos designers.',
            'desc_ar': 'أبحاث المستخدمين، النماذج الأولية التفاعلية، وأنظمة التصميم الشاملة بطنجة والمغرب. حسن تجربة مستخدمي تطبيقك أو موقعك. تواصل معنا اليوم.',
        },
        'api-microservices': {
            'title_en': 'API & Microservices in Tangier, Morocco | getNexiro',
            'title_fr': 'API & Microservices à Tanger, Maroc | getNexiro',
            'title_ar': 'واجهات برمجة التطبيقات بطنجة | getNexiro',
            'desc_en': 'Robust RESTful and GraphQL API architecture, microservices engineering, and third-party integrations in Tangier, Morocco. Start your API project now.',
            'desc_fr': "Architecture d'API RESTful et GraphQL, microservices robustes et intégrations tierces à Tanger, Maroc. Fiabilité et sécurité. Contactez nos architectes.",
            'desc_ar': 'تصميم وتطوير واجهات برمجة التطبيقات REST وGraphQL وبنيات الخدمات المصغرة بطنجة والمغرب. تكامل سلس وسرعة استجابة. ابدأ مشروعك التقني معنا.',
        },
        'cloud-devops': {
            'title_en': 'Cloud & DevOps in Tangier, Morocco | getNexiro',
            'title_fr': 'Cloud & DevOps à Tanger, Maroc | getNexiro',
            'title_ar': 'خدمات السحابة وديف أوبس بطنجة | getNexiro',
            'desc_en': 'Cloud infrastructure engineering, automated CI/CD pipelines, Docker containerization, and monitoring in Tangier, Morocco. Optimize your stack today.',
            'desc_fr': 'Infrastructures cloud sécurisées, pipelines CI/CD automatisés, conteneurisation Docker et monitoring à Tanger, Maroc. Optimisez votre infrastructure.',
            'desc_ar': 'إدارة البنية التحتية السحابية، أتمتة خطوط النشر CI/CD، وحاويات دوكر ومراقبة الأداء بطنجة والمغرب. عزز استقرار أنظمتك وتواصل معنا الآن.',
        },
        'technical-consulting': {
            'title_en': 'Technical Consulting in Tangier, Morocco | getNexiro',
            'title_fr': 'Conseil Technique à Tanger, Maroc | getNexiro',
            'title_ar': 'الاستشارات التقنية في طنجة، المغرب | getNexiro',
            'desc_en': 'Architecture audits, technology stack selection, and digital transformation consulting in Tangier, Morocco. Make sound tech choices. Schedule a session.',
            'desc_fr': "Audits d'architecture, sélection de stack technique et conseil en transformation numérique à Tanger, Maroc. Prenez rendez-vous avec nos consultants.",
            'desc_ar': 'تدقيق معماريات البرمجيات، اختيار حزم التقنيات المناسبة، واستشارات التحول الرقمي بطنجة والمغرب. اتخذ قرارات تقنية سليمة وتواصل معنا اليوم.',
        },
    }

    for slug, meta in service_metadata.items():
        Service.objects.filter(slug=slug).update(
            seo_title_en=meta['title_en'],
            seo_title_fr=meta['title_fr'],
            seo_title_ar=meta['title_ar'],
            seo_description_en=meta['desc_en'],
            seo_description_fr=meta['desc_fr'],
            seo_description_ar=meta['desc_ar'],
        )

    # 3. Projects
    for prj in Project.objects.all():
        sector = prj.category.name_en if prj.category else 'Tech'
        short_title = prj.title_en.split('—')[0].strip()
        t_en = f"{short_title} — {sector} Case Study | getNexiro"
        if len(t_en) > 60:
            t_en = f"{short_title} Case Study | getNexiro"
        if len(t_en) > 60:
            t_en = f"{short_title[:45]} | getNexiro"

        t_fr = f"{short_title} — Étude de Cas {sector} | getNexiro"
        if len(t_fr) > 60:
            t_fr = f"{short_title} — Cas Client | getNexiro"
        if len(t_fr) > 60:
            t_fr = f"{short_title[:45]} | getNexiro"

        t_ar = f"{short_title} — دراسة حالة {sector} | getNexiro"
        if len(t_ar) > 60:
            t_ar = f"{short_title} — دراسة حالة | getNexiro"
        if len(t_ar) > 60:
            t_ar = f"{short_title[:45]} | getNexiro"

        d_en = f"Case study on {short_title} engineered by getNexiro in Tangier, Morocco. Learn about our architecture, solutions, and measurable business impact."
        if len(d_en) > 155:
            d_en = d_en[:154] + '.'
        elif len(d_en) < 120:
            d_en += " Contact our engineering team for details."

        d_fr = f"Étude de cas sur {short_title} conçu par getNexiro à Tanger au Maroc. Découvrez notre approche technique, nos solutions et les résultats concrets."
        if len(d_fr) > 155:
            d_fr = d_fr[:154] + '.'
        elif len(d_fr) < 120:
            d_fr += " Contactez notre équipe pour en savoir plus."

        d_ar = f"دراسة حالة لمشروع {short_title} من تنفيذ استوديو getNexiro بطنجة، المغرب. تعرف على الحلول الهندسية والنتائج التشغيلية المحققة بالتفصيل."
        if len(d_ar) > 155:
            d_ar = d_ar[:154] + '.'
        elif len(d_ar) < 120:
            d_ar += " تواصل مع فريقنا لمناقشة مشروعك."

        Project.objects.filter(pk=prj.pk).update(
            seo_title_en=t_en,
            seo_title_fr=t_fr,
            seo_title_ar=t_ar,
            seo_description_en=d_en,
            seo_description_fr=d_fr,
            seo_description_ar=d_ar,
        )

    # 4. City pages
    for cp in CityServicePage.objects.all():
        city_name_en = cp.get_city_display()
        service_name_en = cp.service.title_en if cp.service else 'Web Development'
        service_name_fr = cp.service.title_fr if cp.service and cp.service.title_fr else 'Développement Web'
        service_name_ar = cp.service.title_ar if cp.service and cp.service.title_ar else 'تطوير المواقع'

        t_en = f"{service_name_en} in {city_name_en} | getNexiro"
        if len(t_en) > 60:
            t_en = f"{service_name_en[:35]} in {city_name_en} | getNexiro"

        t_fr = f"{service_name_fr} à {city_name_en} | getNexiro"
        if len(t_fr) > 60:
            t_fr = f"{service_name_fr[:35]} à {city_name_en} | getNexiro"

        t_ar = f"{service_name_ar} في {city_name_en} | getNexiro"
        if len(t_ar) > 60:
            t_ar = f"{service_name_ar[:35]} في {city_name_en} | getNexiro"

        d_en = f"Professional {service_name_en.lower()} services for companies in {city_name_en}, delivered by getNexiro. Scalable solutions. Request a free quote today."
        if len(d_en) > 155:
            d_en = d_en[:154] + '.'
        elif len(d_en) < 120:
            d_en += " Contact our team in Tangier to get started."

        d_fr = f"Services experts en {service_name_fr.lower()} pour entreprises à {city_name_en}, réalisés par getNexiro. Demandez votre devis gratuit dès maintenant."
        if len(d_fr) > 155:
            d_fr = d_fr[:154] + '.'
        elif len(d_fr) < 120:
            d_fr += " Contactez nos ingénieurs dès aujourd'hui."

        d_ar = f"خدمات احترافية في {service_name_ar} للشركات في {city_name_en} من استوديو getNexiro. حلول برمجية مخصصة وعالية الأداء. اطلب عرض سعر مجاني اليوم."
        if len(d_ar) > 155:
            d_ar = d_ar[:154] + '.'
        elif len(d_ar) < 120:
            d_ar += " تواصل مع فريقنا الهندسي الآن."

        CityServicePage.objects.filter(pk=cp.pk).update(
            seo_title_en=t_en,
            seo_title_fr=t_fr,
            seo_title_ar=t_ar,
            seo_description_en=d_en,
            seo_description_fr=d_fr,
            seo_description_ar=d_ar,
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_author_blogpost_index_in_sitemap_blogpost_noindex_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_seo_data, noop),
    ]
