from django.db import migrations

def populate_service_deep_content(apps, schema_editor):
    Service = apps.get_model('core', 'Service')
    FAQ = apps.get_model('core', 'FAQ')

    services_data = {
        'web-development': {
            'title_en': 'Web Development in Tangier, Morocco',
            'title_fr': 'Développement Web à Tanger, Maroc',
            'title_ar': 'تطوير مواقع وتطبيقات الويب بطنجة، المغرب',
            'subtitle_en': 'High-velocity web applications, portals & custom B2B platforms engineered for speed and conversion.',
            'subtitle_fr': 'Applications web haute performance, portails et plateformes B2B sur mesure conçus pour la vitesse et la conversion.',
            'subtitle_ar': 'تطبيقات ويب عالية الأداء وبوابات ومنصات رقمية مخصصة للشركات، مبنية للسرعة وتحقيق أعلى معدلات التحويل.',
            'description_en': (
                "getNexiro delivers full-stack web development engineered specifically for modern Moroccan enterprises and international companies seeking premier nearshore engineering in Tangier. "
                "From high-traffic e-commerce ecosystems and specialized patient care portals to complex multi-tenant B2B platforms, every web solution is architected with modern Python/Django and React/Next.js frameworks. "
                "We reject bloated off-the-shelf templates in favor of clean, modular code, resilient PostgreSQL databases, sub-second page loads, and native multilingual localization across English, French, and Arabic with true bidirectional RTL support. "
                "Our development studio operates directly from Tangier, providing immediate regional responsiveness for Northern Morocco businesses while aligning seamlessly with European client working hours in GMT+1."
            ),
            'description_fr': (
                "getNexiro conçoit des solutions de développement web full-stack adaptées aux entreprises marocaines en pleine expansion et aux organisations internationales recherchant l'excellence nearshore à Tanger. "
                "Des plateformes e-commerce à fort trafic aux portails médicaux et applications d'entreprise B2B multi-utilisateurs, chaque projet repose sur les technologies éprouvées Python/Django et React/Next.js. "
                "Nous refusons les modèles préfabriqués pour privilégier une architecture sur mesure, des bases de données PostgreSQL robustes, des temps de chargement ultra-rapides et une localisation multilingue native (français, anglais, arabe avec support RTL rigoureux). "
                "Basée au cœur de Tanger, notre équipe garantit une proximité opérationnelle pour le nord du Maroc et un alignement parfait avec les horaires européens en GMT+1."
            ),
            'description_ar': (
                "تقدم جيت نكسيرو (getNexiro) خدمات تطوير وتصميم مواقع وتطبيقات الويب المتكاملة المخصصة للشركات المغربية الرائدة والمؤسسات الدولية الباحثة عن كفاءات هندسية متميزة في طنجة. "
                "من منصات التجارة الإلكترونية عالية الحركة وبوابات المراكز الطبية إلى المنظومات المؤسسية المتقدمة للشركات، نعتمد على أحدث التقنيات مثل بايثون/دجانغو ورياكت/نكست. "
                "نبتعد تماماً عن القوالب الجاهزة ونبني أنظمة برمجية مصممة خصيصاً بأعلى معايير السرعة والأمان، مع دعم كامل للغات الثلاث: العربية والفرنسية والإنجليزية بتنسيق اتجاه طبيعي وسلس. "
                "انطلاقاً من موقعنا الاستراتيجي بطنجة، نوفر استجابة فورية لشركائنا في شمال المغرب مع تزامن كامل مع مواعيد العمل الأوروبية في توقيت GMT+1."
            ),
            'methodology_en': (
                "Our web engineering workflow follows a rigorous sprint-driven cadence designed for enterprise predictability:\n"
                "1. Architectural Blueprint: Schema modeling, API specification, and security boundaries.\n"
                "2. Component-Driven UI: Atomic design implementation using Tailwind CSS and Next.js.\n"
                "3. Robust Backend Engineering: Django ORM optimization, caching strategies, and RESTful endpoints.\n"
                "4. Automated Quality Assurance: Unit tests, integration tests, WCAG AA accessibility, and Core Web Vitals profiling.\n"
                "5. Zero-Downtime Deployment: Dockerized container releases backed by automated rollback triggers."
            ),
            'methodology_fr': (
                "Notre méthodologie d'ingénierie web repose sur un cycle itératif garantissant transparence et respect des délais :\n"
                "1. Cadrage & Architecture : Modélisation des bases de données, contrats d'API et protocoles de sécurité.\n"
                "2. Interface Orientée Composants : Développement atomic design via Tailwind CSS et Next.js.\n"
                "3. Ingénierie Backend : Optimisation Django ORM, stratégies de cache Redis et points d'accès REST.\n"
                "4. Assurance Qualité Automatisée : Tests unitaires, accessibilité WCAG AA et optimisation Core Web Vitals.\n"
                "5. Déploiement Continu : Conteneurisation Docker et mises en production sans interruption de service."
            ),
            'methodology_ar': (
                "تتبع منهجيتنا في هندسة الويب دورة عمل محكمة تضمن الشفافية والدقة في التسليم:\n"
                "1. التخطيط وهندسة النظام: نمذجة قواعد البيانات، تحديد واجهات البرمجة، وبروتوكولات الأمان.\n"
                "2. تطوير واجهات المستخدم: بناء المكونات المرئية الحديثة باستخدام تايلويند ونكست.\n"
                "3. هندسة الخوادم الخلفية: تحسين أداء دجانغو، آليات التخزين المؤقت، وواجهات REST.\n"
                "4. ضمان الجودة التلقائي: اختبارات برمجية شاملة، فحص معايير الوصول وسرعة الأداء.\n"
                "5. النشر والتشغيل الحي: نشر عبر حاويات دوكر مع استمرارية كاملة للخدمة دون انقطاع."
            ),
            'deliverables_en': (
                "Custom Python / Django & Next.js Web Application\n"
                "Normalized PostgreSQL Database Architecture & Migrations\n"
                "Comprehensive Trilingual Localization (EN / FR / AR with Native RTL)\n"
                "Fully Responsive Luxury UI/UX Designed for Mobile & Desktop\n"
                "High-Grade SSL/TLS Configuration & HTTP/3 Optimization\n"
                "Integrated Admin Dashboard for Complete Content & User Control\n"
                "Structured SEO Meta Tags, XML Sitemaps & OpenGraph Tags\n"
                "Automated Daily Offsite Database Backup Script"
            ),
            'deliverables_fr': (
                "Application web sur mesure développée en Python / Django & Next.js\n"
                "Architecture de base de données PostgreSQL normalisée et migrations\n"
                "Localisation trilingue complète (Français, Anglais, Arabe avec support RTL)\n"
                "Interface utilisateur responsive haut de gamme optimisée mobile et bureau\n"
                "Configuration de sécurité SSL/TLS avancée et compatibilité HTTP/3\n"
                "Tableau de bord administrateur sur mesure pour la gestion des contenus\n"
                "Optimisation SEO technique complète, sitemaps XML et balises OpenGraph\n"
                "Sauvegardes automatiques quotidiennes chiffrées hors site"
            ),
            'deliverables_ar': (
                "تطبيق ويب مخصص مبني بأحدث تقنيات بايثون / دجانغو ونكست\n"
                "هندسة قواعد بيانات بوستجريسيل متطورة ومحكمة\n"
                "تعريب وترجمة شاملة لثلاث لغات (العربية، الفرنسية، الإنجليزية)\n"
                "تصميم واجهات راقية متوافقة تماماً مع الهواتف والحواسيب\n"
                "تهيئة بروتوكولات الأمان والتشفير المتقدمة SSL/TLS\n"
                "لوحة تحكم إدارية مرنة لإدارة المحتوى والمستخدمين بسهولة\n"
                "تهيئة محركات البحث المتقدمة، خرائط الموقع وبيانات الميتا\n"
                "نظام نسخ احتياطي تلقائي يومي مشفر لقواعد البيانات"
            ),
            'target_audience_en': (
                "• Northern Morocco Industrial Exporters: Manufacturing and logistics leaders in Tanger Med and TFZ requiring bespoke operational portals.\n"
                "• Medical Clinics & Healthcare Centers: Modern clinics needing HIPAA/CNDP-compliant patient scheduling, results delivery, and intake.\n"
                "• Regional E-Commerce Brands: Retailers seeking bespoke, high-conversion storefronts without Shopify percentage transaction fees.\n"
                "• European Startups & Agencies: Technical teams seeking a dedicated, timezone-aligned nearshore engineering team in Tangier."
            ),
            'target_audience_fr': (
                "• Exportateurs et industriels du Nord : Entreprises de Tanger Med et de la TFZ nécessitant des portails opérationnels sur mesure.\n"
                "• Cliniques et laboratoires médicaux : Centres de santé exigeant des plateformes sécurisées pour les rendez-vous et résultats.\n"
                "• Marques e-commerce régionales : Commerçants souhaitant une plateforme indépendante, performante et sans commissions sur ventes.\n"
                "• Startups et agences européennes : Équipes techniques cherchant un pôle d'ingénierie nearshore dédié et disponible en GMT+1."
            ),
            'target_audience_ar': (
                "• المصدرون والشركات الصناعية: المؤسسات العاملة في طنجة المتوسط والمنطقة الحرة الراغبة في بوابات رقمية لإدارة العمليات.\n"
                "• المصحات والمختبرات الطبية: المراكز الصحية التي تحتاج منصات آمنة لحجز المواعيد وعرض التحاليل الطبية.\n"
                "• المتاجر والعلامات التجارية: الشركات الراغبة في متاجر إلكترونية مستقلة وسريعة بدون عمولات على المبيعات.\n"
                "• الشركات والوكالات الأوروبية: فرق العمل التقنية الباحثة عن شريك برمجي موثوق في نفس التوقيت الزمني بطنجة."
            ),
            'process_steps_en': (
                "Step 1: Discovery & Strategy (Weeks 1–2) — Domain analysis, workflow audit, and architecture scoping.\n"
                "Step 2: UI/UX Wireframing & Prototyping (Weeks 2–3) — Interactive design reviews and design tokens.\n"
                "Step 3: Core Sprint Development (Weeks 4–7) — Database models, backend logic, and frontend build.\n"
                "Step 4: Hardening & Testing (Week 8) — Security pentesting, cross-browser validation, and speed audit.\n"
                "Step 5: Production Launch & Retainer Support — Managed deployment, DNS setup, and ongoing SLA maintenance."
            ),
            'process_steps_fr': (
                "Étape 1 : Cadrage & Stratégie (Semaines 1–2) — Analyse des flux métier, choix technologiques et spécifications.\n"
                "Étape 2 : Design UI/UX & Prototypage (Semaines 2–3) — Maquettes interactives et validation des parcours clients.\n"
                "Étape 3 : Développement par Sprints (Semaines 4–7) — Modélisation des données, logique backend et intégration UI.\n"
                "Étape 4 : Tests & Sécurisation (Semaine 8) — Audit de sécurité, tests multi-navigateurs et optimisation des vitesses.\n"
                "Étape 5 : Mise en Ligne & Accompagnement — Déploiement sécurisé, DNS et maintenance évolutive continue."
            ),
            'process_steps_ar': (
                "المرحلة 1: الدراسة والتخطيط (الأسابيع 1-2) — تحليل متطلبات العمل، تحديد البنية التقنية، ودراسة تدفقات المستخدمين.\n"
                "المرحلة 2: تصميم الواجهات وتجربة المستخدم (الأسابيع 2-3) — نماذج تفاعلية مراجعة وتحديد الهوية البصرية.\n"
                "المرحلة 3: التطوير البرمجي (الأسابيع 4-7) — بناء قواعد البيانات، خوارزميات النظام، والربط بالواجهات.\n"
                "المرحلة 4: الاختبار والأمان (الأسبوع 8) — اختبارات الحماية، فحص التوافق عبر الأجهزة، وتحسين السرعة.\n"
                "المرحلة 5: الإطلاق والدعم المستمر — التشغيل على الخوادم الرسمية، ربط النطاقات، وتقديم الدعم الفني."
            ),
            'pricing_guidance_en': (
                "Custom web development projects at getNexiro start from $1,500 (approx. 15,000 MAD) for focused business platforms, ranging to $7,500+ (75,000+ MAD) for complex multi-tier enterprise systems with extensive integrations. "
                "TODO(owner): Confirm final service pricing tiers and quotation guidelines for web development."
            ),
            'pricing_guidance_fr': (
                "Les projets de développement web sur mesure débutent à partir de 15 000 MAD (env. 1 500 $) pour des plateformes d'entreprise ciblées, et jusqu'à 75 000+ MAD pour des applications d'envergure multi-niveaux. "
                "TODO(owner): Confirmer les grilles tarifaires définitives pour le développement web."
            ),
            'pricing_guidance_ar': (
                "تبدأ مشاريع تطوير تطبيقات ومواقع الويب المخصصة لدينا من 15,000 درهم مغربي للمنصات الموجهة للشركات، وتصل إلى 75,000 درهم فأكثر للمنظومات المؤسسية المتقدمة. "
                "TODO(owner): تأكيد المستويات السعرية النهائية لخدمات تطوير الويب."
            ),
            'technologies': 'Django, Python, Next.js, React, PostgreSQL, Tailwind CSS, Docker, Nginx, Redis',
            'timeline': '4 — 8 Weeks',
            'faqs': [
                (
                    "How long does a custom web application take to build?",
                    "Combien de temps faut-il pour créer une application web sur mesure ?",
                    "كم من الوقت يستغرق بناء تطبيق ويب مخصص؟",
                    "A focused web application typically takes between 4 and 8 weeks depending on the complexity of workflows, third-party integrations, and multilingual requirements. We provide milestone schedules with weekly sprint demos.",
                    "Une application web ciblée nécessite généralement entre 4 et 8 semaines selon la complexité des fonctionnalités et les intégrations requises. Nous fournissons des plannings clairs avec des démonstrations hebdomadaires.",
                    "يستغرق تطوير تطبيق ويب مخصص ما بين 4 إلى 8 أسابيع في العادة، اعتماداً على حجم المتطلبات والتكاملات البرمجية. نوفر جدولاً زمنياً دقيقاً وعروضاً أسبوعية للتقدم."
                ),
                (
                    "Can you migrate our existing legacy system without business disruption?",
                    "Pouvez-vous migrer notre système existant sans interruption d'activité ?",
                    "هل يمكنكم نقل نظامنا القديم دون انقطاع سير العمل؟",
                    "Yes. We design parallel data migration pipelines and blue-green deployments to ensure your current operations continue uninterrupted during database and application migration.",
                    "Oui. Nous mettons en place des procédures de migration parallèle des données pour garantir une continuité totale de vos opérations jusqu'à la bascule définitive.",
                    "نعم بكل تأكيد. نصمم خطط نقل بيانات متزامنة تضمن استمرار أعمالكم اليومية دون أي انقطاع حتى اكتمال الترقية بالكامل."
                ),
                (
                    "Do you provide hosting and post-launch maintenance?",
                    "Fournissez-vous l'hébergement et la maintenance post-lancement ?",
                    "هل تقدمون خدمات الاستضافة والصيانة بعد الإطلاق؟",
                    "Yes. We offer fully managed cloud hosting on enterprise infrastructure, daily encrypted backups, uptime monitoring, and proactive security patching under ongoing SLA retainers.",
                    "Oui. Nous proposons un hébergement infogéré sur des infrastructures cloud haute disponibilité, des sauvegardes quotidiennes chiffrées et une maintenance continue sous contrat de service.",
                    "نعم. نقدم خدمات استضافة مدارة بالكامل على خوادم سحابية عالية الأمان، مع نسخ احتياطي يومي مشفر وتحديثات أمنية دورية ودعم فني مستمر."
                ),
                (
                    "How do you handle multilingual websites (Arabic, French, English)?",
                    "Comment gérez-vous les sites web multilingues (Arabe, Français, Anglais) ?",
                    "كيف تديرون المواقع متعددة اللغات (العربية، الفرنسية، الإنجليزية)؟",
                    "We implement native i18n architectural patterns at both the database and frontend levels. Arabic includes dedicated bidirectional RTL stylesheets, proper typographic scales, and natural phrasing—never automatic Google translation.",
                    "Nous intégrons le multilinguisme directement dans le socle technique et la base de données. L'arabe bénéficie d'une feuille de style RTL native et d'une rédaction naturelle, loin des traductions automatiques.",
                    "ندمج اللغات مباشرة في البنية التحتية البرمجية وقواعد البيانات. تحظى اللغة العربية بتنسيق واتجاه طبيعي مخصص (RTL) مع صياغة بشرية متقنة بعيداً عن الترجمة الآلية."
                ),
            ]
        },
        'mobile-applications': {
            'title_en': 'Mobile Applications in Tangier, Morocco',
            'title_fr': 'Développement d\'Applications Mobiles à Tanger, Maroc',
            'title_ar': 'تطوير تطبيقات الهواتف الذكية بطنجة، المغرب',
            'subtitle_en': 'High-performance cross-platform iOS and Android apps engineered with Flutter and modern native stacks.',
            'subtitle_fr': 'Applications mobiles iOS et Android haute performance développées avec Flutter et les technologies natives.',
            'subtitle_ar': 'تطبيقات هواتف ذكية فائقة الأداء لمنصتي iOS و Android مبنية بأحدث تقنيات فلاتر والبرمجة الأصيلة.',
            'description_en': (
                "getNexiro crafts robust, consumer-grade and enterprise mobile applications that run smoothly across both iOS and Android. "
                "Leveraging Flutter and native device capabilities, we build fluid 60fps user interfaces, reliable offline-first data synchronization, biometric authentication, push notification systems, and secure mobile payment workflows. "
                "Whether you are digitizing field logistics across the Tangier-Tétouan industrial corridor, launching a patient portal, or developing an innovative consumer product, our mobile engineering ensures unified codebases with native speed and uncompromising stability."
            ),
            'description_fr': (
                "getNexiro conçoit des applications mobiles performantes pour iOS et Android répondant aux exigences des entreprises modernes et des utilisateurs finaux. "
                "Grâce à Flutter et aux technologies natives, nous développons des interfaces fluides à 60fps, une synchronisation hors-ligne intelligente, l'authentification biométrique, les notifications push et l'intégration de passerelles de paiement sécurisées. "
                "Qu'il s'agisse d'optimiser la logistique de terrain dans le nord du Maroc ou de lancer un service grand public, nous garantissons une expérience utilisateur irréprochable et un code pérenne."
            ),
            'description_ar': (
                "تبتكر جيت نكسيرو (getNexiro) تطبيقات هواتف ذكية قوية ومتطورة لمنصتي آيفون وأندرويد تلبي تطلعات الشركات الحديثة والمستخدمين. "
                "بالاعتماد على تقنية فلاتر المتقدمة، نطور واجهات استخدام فائقة السلاسة، مع إمكانية العمل دون اتصال بالإنترنت والمزامنة الفورية، والمصادقة بالبصمة، والإشعارات الفورية، والربط مع بوابات الدفع الإلكتروني المعتمدة في المغرب ودولياً. "
                "سواء كنتم تديرون عمليات لوجستية وصناعية في جهة طنجة تطوان أو تطلقون خدمة مبتكرة، نضمن لكم تطبيقاً سريعاً ومستقراً بأعلى درجات الأمان."
            ),
            'methodology_en': (
                "Our mobile development pipeline ensures high test coverage and swift app store approvals:\n"
                "1. User Journey & Touch Optimization: Micro-interactions and touch targets designed for mobile Ergonomics.\n"
                "2. Cross-Platform Flutter Core: Shared business logic with device-specific platform channels.\n"
                "3. Offline-First Architecture: Local storage caching with conflict-free background synchronization.\n"
                "4. Multi-Device Physical Lab Testing: Rigorous QA across diverse screen ratios and operating systems.\n"
                "5. App Store & Play Store Publishing: End-to-end handling of certificates, provisioning profiles, and compliance audits."
            ),
            'methodology_fr': (
                "Notre processus de développement mobile garantit robustesse et publication fluide sur les stores :\n"
                "1. Ergonomie Mobile : Conception de parcours fluides et micro-interactions adaptées aux écrans tactiles.\n"
                "2. Développement Flutter Unifié : Logique métier partagée et intégration fine des composants natifs.\n"
                "3. Architecture Hors-Ligne : Mise en cache locale et synchronisation intelligente lors du retour réseau.\n"
                "4. Tests sur Appareils Réels : Validation rigoureuse sur un parc varié de smartphones et versions d'OS.\n"
                "5. Déploiement App Store & Google Play : Gestion intégrale des certificats, fiches et validations éditeurs."
            ),
            'methodology_ar': (
                "تعتمد دورة تطوير التطبيقات لدينا على الدقة والاختبار الشامل لضمان سهولة الاعتماد في المتاجر:\n"
                "1. تجربة المستخدم والتفاعل: تصميم مسارات بديهية ومريحة للاستخدام باللمس على شاشات الهواتف.\n"
                "2. التطوير الموحد عبر فلاتر: كود برمجي موحد مع استغلال أمثل لمكونات الجهاز الأصيلة.\n"
                "3. العمل دون إنترنت: حفظ البيانات محلياً مع المزامنة التلقائية فور عودة الاتصال.\n"
                "4. الفحص على هواتف متعددة: تجربة التطبيق على أجهزة متنوعة بمختلف مقاسات الشاشات وأنظمة التشغيل.\n"
                "5. النشر في متجري آب ستور وجوجل بلاي: إدارة شاملة لإجراءات الاعتماد وتوثيق الحسابات الرسمية."
            ),
            'deliverables_en': (
                "Production iOS Application (IPA) configured for Apple App Store\n"
                "Production Android Application (AAB/APK) configured for Google Play\n"
                "Unified Flutter / Dart Cross-Platform Codebase\n"
                "Secure REST / GraphQL Backend API Integration with Token Authentication\n"
                "Push Notification Service Integration (Firebase Cloud Messaging)\n"
                "Integrated Crash Analytics & Performance Telemetry\n"
                "Offline Caching Engine with Conflict-Resolution Protocol\n"
                "Complete Store Submission & Review Approval Support"
            ),
            'deliverables_fr': (
                "Application iOS prête pour l'App Store d'Apple (paquet IPA)\n"
                "Application Android prête pour Google Play Store (paquet AAB/APK)\n"
                "Code source complet unifié en Flutter / Dart\n"
                "Intégration API backend sécurisée avec authentification par jeton (JWT)\n"
                "Configuration des notifications push (Firebase Cloud Messaging)\n"
                "Tableau de bord de suivi des performances et remontée des anomalies\n"
                "Moteur de cache hors-ligne avec synchronisation automatique\n"
                "Accompagnement complet jusqu'à la validation officielle sur les stores"
            ),
            'deliverables_ar': (
                "تطبيق iOS معتمد وجاهز لمتجر آبل ستور (IPA)\n"
                "تطبيق أندرويد جاهز لمتجر جوجل بلاي (AAB/APK)\n"
                "الكود المصدري الكامل الموحد بتقنية فلاتر\n"
                "ربط كامل وآمن مع واجهات الخادم البرمجية API\n"
                "خدمة إرسال الإشعارات الفورية للزبائن عبر فايربيس\n"
                "نظام رصد الأعطال وتحليل سرعة وأداء التطبيق\n"
                "محرك تخزين محلي للعمل دون اتصال بالشبكة\n"
                "متابعة مستمرة لعملية المراجعة والموافقة على النشر بالمتجرين"
            ),
            'target_audience_en': (
                "• Field Services & Logistics Operators: Transportation fleets in Northern Morocco needing real-time dispatch and driver tracking.\n"
                "• Healthcare & Telehealth Providers: Clinics offering patient appointment booking, doctor chat, and test result delivery.\n"
                "• Retailers & On-Demand Delivery: Local brands launching customer ordering, loyalty programs, and instant courier assignment.\n"
                "• Scaleups & Digital Innovators: Entrepreneurs requiring high-velocity cross-platform MVPs with scalable backends."
            ),
            'target_audience_fr': (
                "• Transporteurs et logisticiens : Flottes et équipes de terrain à Tanger et dans le Nord nécessitant un suivi temps réel.\n"
                "• Professionnels de santé : Établissements souhaitant proposer la prise de rendez-vous et le suivi des dossiers patients sur mobile.\n"
                "• Commerces et livraison express : Enseignes développant la commande en ligne, programmes de fidélité et suivi de livraison.\n"
                "• Créateurs d'entreprises innovantes : Porteurs de projet recherchant un MVP mobile multiplateforme performant et évolutif."
            ),
            'target_audience_ar': (
                "• شركات النقل واللوجستيك: الأساطيل وفرق الميدان في طنجة والشمال التي تحتاج تتبعاً وإدارة فورية للعمليات.\n"
                "• المراكز الطبية والعيادات: المؤسسات الصحية الراغبة في توفير حجز المواعيد ومتابعة الملفات الطبية عبر الهاتف.\n"
                "• المتاجر وخدمات التوصيل: الأنشطة التجارية التي تسعى لتقديم طلبات الشراء عبر التطبيق وبرامج الوفاء للزبائن.\n"
                "• رواد الأعمال والشركات الناشئة: أصحاب المشاريع الرقمية الطامحين لإطلاق تطبيق سريع ومتكامل على كل الهواتف."
            ),
            'process_steps_en': (
                "Step 1: Scoping & UX Mapping (Weeks 1–2) — User personas, screen architecture, and hardware permissions.\n"
                "Step 2: UI Design & Clickable Prototype (Weeks 3–4) — High-fidelity mobile components in Figma.\n"
                "Step 3: Flutter Engineering & API Plumbing (Weeks 5–9) — Core business logic, backend sync, and native channels.\n"
                "Step 4: Device Lab Testing & Security Audit (Weeks 10–11) — QA across physical Android and iOS devices.\n"
                "Step 5: App Store Deployment & Post-Launch Monitoring (Week 12+) — Submission, review guidance, and initial metrics."
            ),
            'process_steps_fr': (
                "Étape 1 : Cadrage & Parcours Utilisateur (Semaines 1–2) — Définition des profils, arborescence et autorisations mobiles.\n"
                "Étape 2 : Design d'Interface & Prototype Figma (Semaines 3–4) — Maquettage haute fidélité et validation ergonomique.\n"
                "Étape 3 : Développement Flutter & Connexion API (Semaines 5–9) — Développement des fonctionnalités et synchronisation.\n"
                "Étape 4 : Tests sur Parc Réel & Sécurité (Semaines 10–11) — Contrôle qualité sur terminaux physiques iOS et Android.\n"
                "Étape 5 : Publication sur les Stores & Suivi (Semaine 12+) — Dépôt officiel, suivi des validations et monitoring."
            ),
            'process_steps_ar': (
                "المرحلة 1: التدقيق وتحديد المسارات (الأسابيع 1-2) — دراسة احتياجات المستخدمين، هيكلة الشاشات، وصلاحيات النظام.\n"
                "المرحلة 2: تصميم الواجهات وتجربة الاستخدام (الأسابيع 3-4) — نماذج مرئية تفاعلية دقيقة عبر فيجما.\n"
                "المرحلة 3: البرمجة الموحدة والربط بالخادم (الأسابيع 5-9) — كتابة الكود عبر فلاتر وتفعيل التزامن مع الخوادم.\n"
                "المرحلة 4: الفحص على الأجهزة الحقيقية (الأسابيع 10-11) — اختبارات الجودة والأمان على هواتف آيفون وأندرويد.\n"
                "المرحلة 5: النشر في المتاجر والمتابعة (الأسبوع 12+) — إرسال التطبيق للمراجعة، وتتبع مؤشرات الاستخدام الأولية."
            ),
            'pricing_guidance_en': (
                "Mobile application engineering projects typically range from $2,500 to $9,000+ (approx. 25,000 to 90,000+ MAD) based on hardware integrations (camera, GPS, BLE), offline sync architecture, and backend scope. "
                "TODO(owner): Confirm final mobile application pricing tiers and timeline expectations."
            ),
            'pricing_guidance_fr': (
                "Les projets d'applications mobiles se situent généralement entre 25 000 et 90 000+ MAD selon la complexité des modules matériels (GPS, biométrie), de la synchronisation hors-ligne et du backend. "
                "TODO(owner): Confirmer les tarifs officiels pour les applications mobiles."
            ),
            'pricing_guidance_ar': (
                "تتراوح تكلفة تطوير تطبيقات الهواتف الذكية عادة بين 25,000 و 90,000 درهم مغربي فأكثر، حسب تعقيد الميزات والربط مع عتاد الهاتف ومستوى العمل دون اتصال. "
                "TODO(owner): تأكيد الأسعار الرسمية لتطوير تطبيقات الهواتف الذكية."
            ),
            'technologies': 'Flutter, Dart, React Native, Swift, Kotlin, Firebase, REST APIs, Fastlane',
            'timeline': '6 — 12 Weeks',
            'faqs': [
                (
                    "Should I choose Flutter or separate native apps for iOS and Android?",
                    "Dois-je choisir Flutter ou deux applications natives distinctes pour iOS et Android ?",
                    "هل من الأفضل اختيار تقنية فلاتر أم بناء تطبيقين منفصلين لكل نظام؟",
                    "For 95% of business applications, Flutter provides native-grade performance (60/120fps) from a single shared codebase, cutting development and maintenance costs by almost half while delivering a pixel-perfect interface on both platforms.",
                    "Dans 95 % des projets professionnels, Flutter offre des performances équivalentes au natif à partir d'un code source unique, réduisant le budget et les délais de près de moitié avec une qualité visuelle irréprochable.",
                    "في الغالبية الساحقة من المشاريع، تمنح تقنية فلاتر سرعة وأداء يضاهي البرمجة الأصلية بكود برمجي موحد، مما يقلل تكاليف التطوير والصيانة إلى النصف مع تقديم تجربة استثنائية."
                ),
                (
                    "Will my app work when users lose their internet connection?",
                    "Mon application fonctionnera-t-elle lorsque les utilisateurs perdent leur connexion internet ?",
                    "هل سيعمل التطبيق عندما يفقد المستخدمون الاتصال بالإنترنت؟",
                    "Yes. We design our mobile applications with offline-first local database caching. Users can view essential data and draft actions offline, which automatically sync with the cloud the moment connectivity resumes.",
                    "Oui. Nous concevons nos applications avec un mode hors-ligne natif. Les utilisateurs continuent de consulter leurs données et d'effectuer des saisies, qui sont synchronisées dès la reconnexion au réseau.",
                    "نعم. نصمم تطبيقاتنا لتعمل دون اتصال بالاعتماد على التخزين المحلي، بحيث يمكن للمستخدم تصفح البيانات وتسجيل المعاملات لتتم مزامنتها تلقائياً بمجرد عودة الاتصال."
                ),
                (
                    "Do you assist with publishing on Google Play and Apple App Store?",
                    "Aidez-vous pour la publication sur Google Play et l'App Store d'Apple ?",
                    "هل تساعدون في عملية النشر والاعتماد على متجري جوجل وآبل؟",
                    "Yes, completely. We manage developer account setup, build generation, privacy disclosures, store assets, and submission review until your application is live and approved.",
                    "Oui, de bout en bout. Nous gérons la configuration des comptes développeurs, la génération des certificats, la conformité RGPD/CNDP et le suivi des validations jusqu'à la mise en ligne effective.",
                    "نعم، بشكل كامل. نتولى إعداد الحسابات، توليد شهادات الحماية، رفع ملفات التطبيق، وإدارة المراجعات حتى صدور الموافقة الرسمية وظهور التطبيق للمستخدمين."
                ),
            ]
        },
        'uiux-design-systems': {
            'title_en': 'UI/UX & Design Systems in Tangier, Morocco',
            'title_fr': 'Design UI/UX & Systèmes Graphiques à Tanger, Maroc',
            'title_ar': 'تصميم واجهات وتجربة المستخدم ونظم التصميم بطنجة، المغرب',
            'subtitle_en': 'Human-centered user experiences, interactive Figma prototypes, and modular design systems.',
            'subtitle_fr': 'Expériences utilisateurs centrées sur l\'humain, prototypes interactifs Figma et design systems modulaires.',
            'subtitle_ar': 'تجارب مستخدم بديهية، نماذج تفاعلية متقدمة عبر فيجما، ونظم تصميم متكاملة وقابلة للتوسع.',
            'description_en': (
                "At getNexiro, UI/UX design is an engineering discipline, not mere decorative styling. "
                "We craft digital interfaces that eliminate user friction, communicate brand authority, and maximize conversion rates. "
                "Our design team creates comprehensive design token systems in Figma, covering typographic hierarchies, contrast-compliant dark and light color palettes, interactive states, and responsive layout grids. "
                "Every component is designed with bidirectional multilingual readiness in mind, guaranteeing that Arabic RTL interfaces look as natural, balanced, and intentional as English and French layouts."
            ),
            'description_fr': (
                "Chez getNexiro, le design UI/UX est abordé avec la rigueur d'une discipline d'ingénierie. "
                "Nous concevons des interfaces digitales intuitives qui suppriment les points de friction, renforcent l'image de marque et maximisent l'engagement client. "
                "Notre studio élabore des design systems complets sous Figma intégrant tokens de design, typographies adaptées, contrastes conformes aux normes WCAG et grilles responsives. "
                "Chaque élément est pensé dès l'origine pour une parité bilingue et trilingue parfaite, assurant à la version arabe en RTL la même élégance et fluidité qu'aux versions française et anglaise."
            ),
            'description_ar': (
                "في جيت نكسيرو (getNexiro)، نعتبر تصميم واجهات وتجربة المستخدم (UI/UX) علماً وهندسة دقيقة تتجاوز مجرد المظهر الجمالي. "
                "نبتكر واجهات رقمية ذكية تلغي التعقيد، تبرز قوة العلامة التجارية، وتحقق أعلى نسب التحويل والتفاعل من الزوار. "
                "يبني فريقنا نظم تصميم (Design Systems) شاملة عبر فيجما، تتضمن معايير الألوان والخطوط والأزرار والمكونات التفاعلية بمختلف حالاتها. "
                "نولي اهتماماً خاصاً لتجربة المستخدم باللغة العربية (RTL) لتكون طبيعية وأصيلة بنفس الفخامة والاتزان المتوفر في اللغتين الفرنسية والإنجليزية."
            ),
            'methodology_en': (
                "Our design process connects user psychology with production code readiness:\n"
                "1. User Research & Information Architecture: User interviews, heuristic reviews, and journey mapping.\n"
                "2. Wireframing & Structural Logic: Low-fidelity wireframes validating information hierarchy.\n"
                "3. Visual Identity & High-Fidelity Design: Dark luxury themes, micro-interactions, and visual contrast.\n"
                "4. Interactive Prototyping: Clickable simulations replicating real application behavior before coding.\n"
                "5. Design Token Delivery: Figma-to-code token specifications for seamless frontend developer implementation."
            ),
            'methodology_fr': (
                "Notre processus de conception relie les besoins utilisateurs aux impératifs du code de production :\n"
                "1. Recherche Utilisateur & Arborescence : Enquêtes, audits heuristiques et cartographie des parcours.\n"
                "2. Wireframing & Structure : Schémas fonctionnels validant la hiérarchie de l'information.\n"
                "3. Identité Visuelle & Haute Fidélité : Univers visuel premium, micro-interactions et accessibilité.\n"
                "4. Prototypage Interactif : Maquettes navigables simulant l'expérience finale avant le développement.\n"
                "5. Transmission des Tokens : Spécifications précises pour une intégration fluide par les développeurs."
            ),
            'methodology_ar': (
                "تربط منهجيتنا في التصميم بين سيكولوجية المستخدم واحتياجات البرمجة الميدانية:\n"
                "1. دراسة سلوك المستخدمين وهندسة المعلومات: مقابلات استطلاعية ورسم مسارات الاستخدام.\n"
                "2. المخططات الهيكلية (Wireframes): تصميم تخطيطي لتحديد أولويات المعلومات وسهولة الوصول.\n"
                "3. التصميم البصري عالي الدقة: اختيار الألوان الراقية، الخطوط المتناسقة، والرسوم التفاعلية.\n"
                "4. النماذج التفاعلية الحية: محاكاة كاملة للتطبيق لاختباره عملياً قبل كتابة أي سطر برمجي.\n"
                "5. تسليم رموز التصميم للمطورين: تصدير المعايير بدقة لتسهيل التحويل إلى كود برمجي مطابق تماماً."
            ),
            'deliverables_en': (
                "Complete Figma Source File with Structured Layer Naming\n"
                "Modular Design System with Reusable UI Components & Variants\n"
                "Documented Design Tokens (Colors, Typography, Spacing, Shadows)\n"
                "Interactive High-Fidelity Clickable Prototype for Stakeholders & Testing\n"
                "Dedicated RTL Layout Specifications for Arabic Translation\n"
                "WCAG 2.1 AA Accessibility Contrast & Typography Compliance Audit\n"
                "Developer Handoff Guide with CSS / Tailwind Utility Mapping\n"
                "Full Export of Vector SVG Assets, Icons, and Visual Guidelines"
            ),
            'deliverables_fr': (
                "Fichier source complet Figma structuré et documenté\n"
                "Design System modulaire avec composants réutilisables et variantes\n"
                "Bibliothèque de Design Tokens (palettes, typographies, espacements, ombres)\n"
                "Prototype interactif haute fidélité pour démonstrations et tests utilisateurs\n"
                "Spécifications complètes pour l'affichage en RTL (arabe)\n"
                "Audit de conformité d'accessibilité WCAG 2.1 AA (contrastes et lisibilité)\n"
                "Guide de transmission développeur avec correspondance des classes Tailwind/CSS\n"
                "Pack complet des icônes vectorielles et éléments graphiques optimisés"
            ),
            'deliverables_ar': (
                "ملف فيجما المصدري الكامل منظم ومبوب باحترافية\n"
                "نظام تصميم معياري متكامل يحتوي كافة المكونات المتكررة وحالاتها\n"
                "دليل رموز التصميم الشامل (الألوان، الخطوط، المسافات، والظلال)\n"
                "نموذج تفاعلي قابل للتجربة والنقر لمحاكاة التطبيق الحقيقي\n"
                "مخططات مخصصة لتنسيق اللغة العربية باتجاه اليمين إلى اليسار (RTL)\n"
                "فحص مطابقة معايير الوصول وسهولة القراءة للجميع (WCAG 2.1 AA)\n"
                "دليل تسليم تقني مفصل يربط التصاميم بأكواد تايلويند وCSS\n"
                "مكتبة الأيقونات والرسومات المتجهة عالية الدقة (SVG)"
            ),
            'target_audience_en': (
                "• Companies Upgrading Legacy Software: Enterprises with clunky internal tools needing modern, intuitive workflows.\n"
                "• Medical & Healthcare Platforms: Diagnostic centers needing clean, patient-friendly interfaces that reduce anxiety.\n"
                "• SaaS Startups & Scaleups: Digital platforms aiming for premium market positioning through exceptional product design.\n"
                "• Regional Brands: Companies seeking distinctive visual identity and polished multilingual presentation."
            ),
            'target_audience_fr': (
                "• Entreprises modernisant leurs logiciels internes : Sociétés souhaitant remplacer des outils vieillissants par des interfaces intuitives.\n"
                "• Plateformes de santé et laboratoires : Établissements exigeant des espaces patients clairs et rassurants.\n"
                "• Startups et éditeurs SaaS : Produits digitaux voulant se démarquer par une expérience utilisateur irréprochable.\n"
                "• Marques régionales : Enseignes souhaitant affirmer une présence numérique élégante et professionnelle."
            ),
            'target_audience_ar': (
                "• الشركات الراغبة في تجديد أنظمتها: المؤسسات التي تعاني من برمجيات قديمة ومعقدة وتريد واجهات حديثة وسريعة.\n"
                "• القطاع الطبي ومراكز الرعاية: المصحات التي تحتاج واجهات سهلة وواضحة للمرضى ومراجعي الخدمات.\n"
                "• منصات الخدمات والبرمجيات SaaS: المشاريع الرقمية الساعية للتميز وجذب المشتركين بتصميم استثنائي.\n"
                "• العلامات التجارية المحلية والإقليمية: الشركات الطامحة لمظهر رقمي فاخر يعكس الثقة والمصداقية."
            ),
            'process_steps_en': (
                "Step 1: Research & Discovery (Week 1) — User interviews, brand alignment, and competitor benchmark.\n"
                "Step 2: Information Architecture & Wireframing (Weeks 1–2) — Content hierarchy and flow validation.\n"
                "Step 3: Visual Design & Design Tokens (Weeks 2–4) — High-fidelity screens and dark luxury aesthetics.\n"
                "Step 4: Interactive Prototype & Usability Testing (Week 5) — Clickable simulation and refinement.\n"
                "Step 5: Developer Handoff & Implementation Support (Week 6) — CSS specs and engineering alignment."
            ),
            'process_steps_fr': (
                "Étape 1 : Recherche & Cadrage (Semaine 1) — Entretiens, analyse concurrentielle et alignement de marque.\n"
                "Étape 2 : Arborescence & Wireframing (Semaines 1–2) — Hiérarchie du contenu et validation des parcours.\n"
                "Étape 3 : Design Visuel & Tokens (Semaines 2–4) — Écrans finaux haute fidélité et univers graphique.\n"
                "Étape 4 : Prototypage & Tests Utilisateurs (Semaine 5) — Validation sur maquette interactive.\n"
                "Étape 5 : Transmission aux Développeurs (Semaine 6) — Export des tokens, classes CSS et accompagnement."
            ),
            'process_steps_ar': (
                "المرحلة 1: البحث والاستكشاف (الأسبوع 1) — دراسة المنافسين، تحديد الهوية، وفهم جمهور المنصة.\n"
                "المرحلة 2: هندسة المعلومات والمخططات (الأسابيع 1-2) — ترتيب الأولويات وتحديد مسارات الاستخدام.\n"
                "المرحلة 3: التصميم البصري ونظم الألوان (الأسابيع 2-4) — ابتكار الواجهات النهائية بالأسلوب الراقي المتناسق.\n"
                "المرحلة 4: النموذج التفاعلي والفحص (الأسبوع 5) — محاكاة تجربة الاستخدام وضبط الملاحظات الدقيقة.\n"
                "المرحلة 5: تسليم الملفات للمطورين (الأسبوع 6) — تصدير مواصفات الكود والتنسيقات للبدء في البرمجة."
            ),
            'pricing_guidance_en': (
                "Comprehensive UI/UX design packages and design system creation range from $1,200 to $4,500 (approx. 12,000 to 45,000 MAD) depending on screen count, user flows, and interactive prototyping scope. "
                "TODO(owner): Confirm final design system pricing tiers and asset handoff packages."
            ),
            'pricing_guidance_fr': (
                "Les forfaits de conception UI/UX et création de design system s'échelonnent entre 12 000 et 45 000 MAD selon le nombre d'écrans, la complexité des parcours et le niveau d'interactivité du prototype. "
                "TODO(owner): Valider les forfaits officiels pour les prestations UI/UX."
            ),
            'pricing_guidance_ar': (
                "تبدأ باقات تصميم واجهات وتجربة المستخدم ونظم التصميم من 12,000 إلى 45,000 درهم مغربي، حسب عدد الشاشات وتعقيد النماذج التفاعلية. "
                "TODO(owner): تأكيد الباقات السعرية النهائية لخدمات التصميم."
            ),
            'technologies': 'Figma, Tokens Studio, Adobe Creative Cloud, Tailwind CSS, Radix UI, Storybook',
            'timeline': '3 — 6 Weeks',
            'faqs': [
                (
                    "What formats and source files do you deliver upon completion?",
                    "Quels formats et fichiers sources livrez-vous à la fin du projet ?",
                    "ما هي صيغ الملفات التي نتسلمها عند انتهاء المشروع؟",
                    "You receive full ownership of the structured Figma file with editable components, design tokens, responsive breakpoints, an interactive clickable prototype URL, and production-ready vector assets (SVG).",
                    "Vous recevez la pleine propriété du fichier Figma complet avec composants modifiables, tokens de design, prototype interactif et assets vectoriels prêts à l'intégration.",
                    "تتسلمون الملكية الكاملة لملف فيجما المصدري المنظم شاملاً المكونات القابلة للتعديل، رموز التصميم، رابط النموذج التفاعلي، وكافة الأيقونات والرسومات بصيغتها الأصلية."
                ),
                (
                    "How do you design for Arabic RTL interfaces?",
                    "Comment concevez-vous les interfaces pour la langue arabe (RTL) ?",
                    "كيف تتعاملون مع تصميم واجهات اللغة العربية من اليمين إلى اليسار؟",
                    "We design dedicated RTL layout grids rather than merely mirroring components. We ensure proper Arabic typography scales (using fonts like Cairo), appropriate icon directionality, and natural reading flows.",
                    "Nous concevons des grilles RTL dédiées plutôt que de simples inversions d'écrans. Nous soignons la typographie arabe (polices adaptées comme Cairo), le sens des icônes et le confort de lecture naturel.",
                    "لا نكتفي بعكس الشاشات آلياً، بل نبني تخطيطاً مخصصاً يراعي قواعد القراءة العربية والخطوط المريحة للعين (مثل خط Cairo) مع ضبط اتجاهات الأيقونات بدقة متناهية."
                ),
            ]
        },
        'api-microservices': {
            'title_en': 'API & Microservices in Tangier, Morocco',
            'title_fr': 'Développement d\'APIs & Microservices à Tanger, Maroc',
            'title_ar': 'تطوير واجهات برمجة التطبيقات والخدمات المصغرة بطنجة، المغرب',
            'subtitle_en': 'High-concurrency RESTful and GraphQL APIs, backend microservices, and seamless enterprise system integrations.',
            'subtitle_fr': 'APIs REST et GraphQL haute performance, microservices robustes et intégrations sécurisées de systèmes d\'entreprise.',
            'subtitle_ar': 'واجهات برمجة تطبيقات REST و GraphQL عالية السرعة، وبنى تحتية للخدمات المصغرة وربط الأنظمة المؤسسية.',
            'description_en': (
                "getNexiro engineers scalable, secure, and resilient API architectures that power complex modern ecosystems. "
                "Whether orchestrating supply chain data exchange through the Tanger Med logistics corridor, connecting custom frontends to legacy ERP systems, or building fintech-grade payment conduits, our backends deliver guaranteed sub-100ms response times and bulletproof reliability. "
                "We implement OpenAPI 3.0 documented REST and GraphQL endpoints using Django Ninja and Python, safeguarded by OAuth2/JWT token authentication, intelligent rate limiting, Redis caching tiers, and asynchronous task workers."
            ),
            'description_fr': (
                "getNexiro conçoit des architectures d'APIs sécurisées et évolutives au cœur des écosystèmes informatiques modernes. "
                "Qu'il s'agisse d'automatiser les échanges de données logistiques avec Tanger Med, d'interconnecter des applications métier à un ERP existant ou d'intégrer des passerelles de paiement bancaires, nous garantissons des temps de réponse ultra-rapides et une fiabilité éprouvée. "
                "Nous développons des APIs REST et GraphQL documentées sous OpenAPI 3.0, protégées par authentification OAuth2/JWT, limitation de débit et files de traitement asynchrones Celery/Redis."
            ),
            'description_ar': (
                "تقوم جيت نكسيرو (getNexiro) بهندسة وتطوير واجهات برمجة التطبيقات (APIs) والخدمات المصغرة التي تشكل العمود الفقري للأنظمة الرقمية الحديثة. "
                "سواء كنتم تديرون تبادل البيانات اللوجستية عبر ميناء طنجة المتوسط، أو تربطون تطبيقاتكم بأنظمة إدارة المؤسسات (ERP)، أو تفعلون بوابات الدفع الإلكتروني، نضمن لكم أداءً فائق السرعة واستقراراً تاماً. "
                "نطور واجهات برمجية موثقة وفق معايير OpenAPI 3.0 ومحمية بأعلى بروتوكولات الأمان والمصادقة الرقمية مع معالجة سريعة للمهام المعقدة في الخلفية."
            ),
            'methodology_en': (
                "Our backend engineering workflow prioritizes data integrity and high-throughput reliability:\n"
                "1. Data Contract & Schema Modeling: Strict domain boundary definition and OpenAPI specifications.\n"
                "2. Asynchronous Architecture: Decoupling intensive computations via Celery and Redis queues.\n"
                "3. Database Optimization: Query plan analysis, composite indexing, and connection pooling in PostgreSQL.\n"
                "4. Security & Access Control: Granular role-based permissions, JWT rotation, and API key rate-limiting.\n"
                "5. Automated Load & Stress Testing: Validating concurrency under simulated enterprise traffic spikes."
            ),
            'methodology_fr': (
                "Notre ingénierie backend garantit intégrité des données et capacité de montée en charge :\n"
                "1. Spécification des Schémas : Définition rigoureuse des contrats d'échange et documentation OpenAPI.\n"
                "2. Traitements Asynchrones : Découplage des tâches lourdes via files d'attente Celery et Redis.\n"
                "3. Optimisation Base de Données : Indexation avancée, requêtes optimisées et pool de connexions PostgreSQL.\n"
                "4. Sécurité & Contrôle d'Accès : Gestion fine des rôles, rotation de jetons JWT et limitation du débit.\n"
                "5. Tests de Charge Automatisés : Validation de la stabilité lors de pics d'utilisation intensifs."
            ),
            'methodology_ar': (
                "تركز هندستنا للخوادم الخلفية على سلامة البيانات والقدرة على التعامل مع آلاف الطلبات المتزامنة:\n"
                "1. تخطيط وتوثيق الواجهات: تحديد عقود البيانات بدقة وتوثيقها وفق معيار OpenAPI.\n"
                "2. المعالجة غير المتزامنة: تفريغ المهام الكبيرة عبر طوابير عمل سريعة باستخدام Redis و Celery.\n"
                "3. تسريع قواعد البيانات: إنشاء الفهارس الذكية، وتحسين استعلامات PostgreSQL لمنع أي بطء.\n"
                "4. الأمان وتحديد الصلاحيات: مصادقة محمية عبر رموز JWT، وتحديد معدل الطلبات لحماية السيرفر.\n"
                "5. اختبارات الضغط والتحمل: محاكاة تدفق آلاف الزوار في نفس اللحظة للتأكد من ثبات النظام."
            ),
            'deliverables_en': (
                "OpenAPI 3.0 / Swagger Interactive API Documentation\n"
                "High-Throughput REST and GraphQL Endpoints Built with Python & Django\n"
                "Secure OAuth2 / JWT Authentication Flow with Refresh Token Rotation\n"
                "Granular Rate-Limiting & Distributed Throttling Engine\n"
                "Asynchronous Background Job Architecture (Celery & Redis)\n"
                "Comprehensive Automated Integration & Endpoint Test Suite\n"
                "Structured JSON Logging & Real-Time Exception Alerting\n"
                "Third-Party ERP, CRM, and Payment Gateway Integration Bridges"
            ),
            'deliverables_fr': (
                "Documentation d'API interactive conforme aux standards OpenAPI 3.0 / Swagger\n"
                "Points de terminaison REST et GraphQL haute performance développés en Python & Django\n"
                "Gestion d'authentification sécurisée OAuth2 / JWT avec renouvellement automatique\n"
                "Système de limitation de débit (rate limiting) pour la protection contre les abus\n"
                "Architecture de tâches de fond asynchrones avec Celery et Redis\n"
                "Suite complète de tests d'intégration automatisés pour chaque endpoint\n"
                "Système de journalisation structurée JSON et alertes d'erreurs en temps réel\n"
                "Connecteurs d'intégration sur mesure avec ERP, CRM et passerelles bancaires"
            ),
            'deliverables_ar': (
                "توثيق تفاعلي كامل لواجهات البرمجة وفق معايير OpenAPI 3.0 / Swagger\n"
                "واجهات REST و GraphQL سريعة ومبنية بأحدث تقنيات بايثون ودجانغو\n"
                "منظومة مصادقة وتشفير متقدمة عبر بروتوكولات OAuth2 و JWT\n"
                "نظام حماية من الضغط الزائد وتحديد معدل الطلبات لكل مستخدم\n"
                "بنية مهام خلفية غير متزامنة لإنجاز العمليات الكبيرة بسلاسة\n"
                "مجموعة اختبارات برمجية مؤتمتة للتأكد من عمل كافة المنافذ بدقة\n"
                "سجلات مراقبة فورية وإشعارات لحظية عند حدوث أي خطأ\n"
                "وحدات ربط متكاملة مع أنظمة الشركات ERP وبوابات الدفع الإلكتروني"
            ),
            'target_audience_en': (
                "• Logistics & Transport Operators: Companies in Tangier Med managing customs, manifest, and fleet tracking APIs.\n"
                "• Financial & Payment Gateways: Businesses integrating multi-currency processing and automated reconciliation.\n"
                "• Multi-Platform Software Providers: Organizations needing a unified, single source of truth backend for web and mobile.\n"
                "• Manufacturing & Supply Chains: Factories in TFZ connecting IoT sensors and warehouse management to cloud databases."
            ),
            'target_audience_fr': (
                "• Opérateurs logistiques et maritimes : Entreprises de Tanger Med gérant des flux de données et manifestes en temps réel.\n"
                "• Services financiers et marchands : Sociétés intégrant le paiement en ligne et la réconciliation bancaire automatisée.\n"
                "• Éditeurs multi-écrans : Structures nécessitant une source de données unique et centralisée pour web et mobile.\n"
                "• Sites industriels et usines de la TFZ : Entreprises reliant équipements industriels et gestion de stock au cloud."
            ),
            'target_audience_ar': (
                "• شركات النقل واللوجستيك بطنجة المتوسط: المنشآت التي تدير بيانات الشحن والجمارك في الوقت الحقيقي.\n"
                "• قطاع المدفوعات والخدمات المالية: الشركات التي تدمج بوابات الدفع وتسوية المعاملات آلياً.\n"
                "• المنصات متعددة التطبيقات: الشركات التي تحتاج خادماً مركزياً موحداً يغذي الموقع والهواتف معاً.\n"
                "• المصانع بالمنطقة الحرة بطنجة: المصانع الراغبة في ربط أجهزة الإنتاج والمخازن بالسحابة الرقمية."
            ),
            'process_steps_en': (
                "Step 1: Domain Modeling & Protocol Scoping (Weeks 1–2) — Endpoint contracts, payloads, and auth strategy.\n"
                "Step 2: Database Modeling & Indexing (Week 3) — Relational constraints and migration setup.\n"
                "Step 3: Core API Construction (Weeks 4–6) — Business logic, serialization, and error handling.\n"
                "Step 4: Load Testing & Security Hardening (Week 7) — Penetration testing, rate limiting, and caching.\n"
                "Step 5: Deployment & Monitoring (Week 8+) — Gateway setup, telemetry tracking, and ongoing maintenance."
            ),
            'process_steps_fr': (
                "Étape 1 : Modélisation Métier & Contrats d'API (Semaines 1–2) — Définition des formats de données et sécurité.\n"
                "Étape 2 : Structure Base de Données (Semaine 3) — Modèles relationnels et stratégies d'indexation.\n"
                "Étape 3 : Développement des Endpoints (Semaines 4–6) — Logique métier, sérialisation et gestion d'erreurs.\n"
                "Étape 4 : Tests de Charge & Sécurité (Semaine 7) — Tests d'intrusion, contrôle des débits et mise en cache.\n"
                "Étape 5 : Déploiement & Télémétrie (Semaine 8+) — Mise en service, surveillance continue et support."
            ),
            'process_steps_ar': (
                "المرحلة 1: النمذجة وتحديد البروتوكولات (الأسابيع 1-2) — صياغة مسارات البيانات وبروتوكولات الأمان.\n"
                "المرحلة 2: هندسة قواعد البيانات (الأسبوع 3) — تصميم الجداول والفهارس لضمان السرعة الفائقة.\n"
                "المرحلة 3: بناء الواجهات البرمجية (الأسابيع 4-6) — برمجة الوظائف، معالجة البيانات، والتحقق من الأخطاء.\n"
                "المرحلة 4: اختبارات الضغط والحماية (الأسبوع 7) — فحص الثغرات، اختبار التحمل، وتفعيل الكاش.\n"
                "المرحلة 5: الإطلاق والمراقبة الحية (الأسبوع 8+) — التشغيل الرسمي، تتبع مؤشرات الأداء، والدعم المستمر."
            ),
            'pricing_guidance_en': (
                "Custom API architecture and microservice integration projects typically range from $1,800 to $6,500 (approx. 18,000 to 65,000 MAD) depending on endpoint complexity, legacy integrations, and throughput SLAs. "
                "TODO(owner): Confirm final API service pricing tiers and integration retainers."
            ),
            'pricing_guidance_fr': (
                "Les projets d'architecture API et d'intégration de microservices se situent généralement entre 18 000 et 65 000 MAD selon le nombre de points d'accès et les contraintes de charge. "
                "TODO(owner): Valider les tarifs finaux pour les architectures API."
            ),
            'pricing_guidance_ar': (
                "تبدأ مشاريع تطوير وتكامل واجهات برمجة التطبيقات من 18,000 إلى 65,000 درهم مغربي، حسب عدد المنافذ وحجم التكاملات المطلوبة. "
                "TODO(owner): تأكيد الأسعار الرسمية لخدمات هندسة واجهات البرمجة."
            ),
            'technologies': 'Python, Django Ninja, Django REST Framework, FastAPI, PostgreSQL, Redis, Celery, Docker, GraphQL',
            'timeline': '4 — 8 Weeks',
            'faqs': [
                (
                    "Can you connect our custom software to legacy ERP systems?",
                    "Pouvez-vous connecter notre logiciel sur mesure à des ERP existants ?",
                    "هل تستطيعون ربط برمجياتنا المخصصة بأنظمة إدارة المؤسسات القديمة (ERP)؟",
                    "Yes. We build custom API middleware and synchronization workers that bridge modern cloud applications with legacy ERPs (SAP, Sage, Microsoft Dynamics) through secure, scheduled or webhook-triggered data conduits.",
                    "Oui. Nous développons des couches logicielles intermédiaires (middleware) sécurisées permettant d'interconnecter vos nouveaux outils à des ERP tels que Sage, SAP ou Microsoft Dynamics.",
                    "نعم بكل تأكيد. نبني طبقات وسيطة برمجية آمنة تربط تطبيقاتكم الحديثة بأنظمة ERP الموجودة لديكم (مثل Sage أو SAP) مع نقل فوري للبيانات دون أي تعارض."
                ),
            ]
        },
        'cloud-devops': {
            'title_en': 'Cloud & DevOps in Tangier, Morocco',
            'title_fr': 'Cloud & DevOps à Tanger, Maroc',
            'title_ar': 'الحوسبة السحابية وهندسة ديف أوبس بطنجة، المغرب',
            'subtitle_en': 'Resilient cloud infrastructure, Docker containerization, automated CI/CD pipelines, and zero-downtime deployments.',
            'subtitle_fr': 'Infrastructures cloud résilientes, conteneurisation Docker, pipelines CI/CD automatisés et déploiements sans interruption.',
            'subtitle_ar': 'بنى تحتية سحابية متقدمة، حاويات دوكر، خطوط نشر مؤتمتة CI/CD، وتشغيل مستمر دون أي انقطاع.',
            'description_en': (
                "getNexiro engineers resilient, self-healing cloud environments designed to eliminate server headaches and maximize application uptime. "
                "We transition businesses from fragile shared hosting setups to automated, containerized cloud architectures on AWS, Hetzner, and dedicated infrastructure. "
                "By orchestrating multi-stage Docker builds, automated GitHub Actions CI/CD pipelines, hardened Nginx reverse proxies, automated SSL renewals, and automated daily offsite encrypted database backups, we give your development team the power to deploy code with total confidence and zero downtime."
            ),
            'description_fr': (
                "getNexiro déploie des environnements cloud résilients et sécurisés pour éliminer les pannes d'infrastructure et garantir une disponibilité maximale de vos services. "
                "Nous accompagnons la transition d'hébergements mutualisés fragiles vers des architectures conteneurisées modernes sur AWS, Hetzner ou serveurs dédiés. "
                "Grâce à Docker, aux pipelines CI/CD automatisés sous GitHub Actions, aux proxys inverses Nginx sécurisés et aux sauvegardes quotidiennes chiffrées hors site, vos équipes déploient en toute sérénité sans interruption de service."
            ),
            'description_ar': (
                "تقدم جيت نكسيرو (getNexiro) حلول الحوسبة السحابية وهندسة ديف أوبس (Cloud & DevOps) المتقدمة المصممة لإنهاء مشاكل الخوادم وضمان استمرار عمل منصاتكم الرقمية على مدار الساعة. "
                "نساعد الشركات على الانتقال من الاستضافات المشتركة الضعيفة إلى بنى تحتية سحابية مستقلة وآمنة عبر خوادم AWS وهتزنر وخوادم خاصة متطورة. "
                "من خلال حاويات دوكر (Docker) وأتمتة النشر عبر GitHub Actions وتهيئة خوادم Nginx المحصنة والنسخ الاحتياطي اليومي المشفر، نضمن لكم إطلاق التحديثات بكل ثقة وأمان."
            ),
            'methodology_en': (
                "Our DevOps engineering adheres to the highest site reliability engineering (SRE) standards:\n"
                "1. Infrastructure Audit & Threat Modeling: Access controls, port hardening, and baseline performance audits.\n"
                "2. Multi-Stage Containerization: Lightweight, reproducible Docker images isolating build dependencies.\n"
                "3. Automated CI/CD Pipelines: Automated linting, test execution, and blue-green server deployment.\n"
                "4. Disaster Recovery & Snapshot Protocols: Automated multi-region encrypted database and asset backups.\n"
                "5. 24/7 Telemetry & Health Monitoring: Real-time alerting for CPU, memory, error rates, and disk thresholds."
            ),
            'methodology_fr': (
                "Notre pratique DevOps respecte les standards stricts de fiabilité des systèmes (SRE) :\n"
                "1. Audit d'Infrastructure & Sécurité : Analyse des accès, fermeture des ports inutiles et contrôle des performances.\n"
                "2. Conteneurisation Docker : Images légères et reproductibles isolant parfaitement chaque brique applicative.\n"
                "3. Pipelines CI/CD Automatisés : Contrôle de code, tests automatisés et mise en production continue.\n"
                "4. Plan de Reprise d'Activité : Sauvegardes chiffrées externalisées et procédures de restauration d'urgence.\n"
                "5. Télémétrie & Surveillance 24/7 : Alertes instantanées sur l'utilisation des ressources et le taux d'erreurs."
            ),
            'methodology_ar': (
                "تتبع ممارساتنا في هندسة ديف أوبس أعلى معايير استقرار وموثوقية الأنظمة السحابية:\n"
                "1. فحص البنية التحتية والأمان: تدقيق المنافذ والصلاحيات وفحص مستوى الأداء الحالي.\n"
                "2. بناء حاويات دوكر المحكمة: عزل بيئة التشغيل بحزم برمجية خفيفة وسريعة التكرار.\n"
                "3. خطوط النشر المؤتمتة (CI/CD): فحص الأكواد واختبارها آلياً قبل تمريرها للخوادم المباشرة.\n"
                "4. خطط الطوارئ والنسخ الاحتياطي: نسخ احتياطي يومي مشفر لقواعد البيانات وحفظه في مواقع جغرافية معزولة.\n"
                "5. المراقبة اللحظية 24/7: إشعارات فورية عند ارتفاع استهلاك الذاكرة أو المعالج للتدخل الاستباقي."
            ),
            'deliverables_en': (
                "Hardened Docker Container Configurations (Multi-Stage Dockerfiles & Compose)\n"
                "Automated GitHub Actions CI/CD Deployment Workflow\n"
                "Nginx Reverse Proxy with HTTP/2, HTTP/3, and SSL/TLS Auto-Renewal\n"
                "Automated Daily Encrypted Offsite Database Backups with Retention Policy\n"
                "Zero-Downtime Blue-Green or Rolling Deployment Setup\n"
                "Server Security Hardening (UFW Firewall, Fail2ban, SSH Key Enforcement)\n"
                "Application Performance Monitoring & Error Alerting Integration\n"
                "Disaster Recovery Runbook with Step-by-Step Restoration Protocols"
            ),
            'deliverables_fr': (
                "Fichiers de conteneurisation Docker multi-étapes et Docker Compose sécurisés\n"
                "Pipeline CI/CD complet automatisé avec GitHub Actions\n"
                "Configuration Nginx reverse proxy avec HTTP/2, HTTP/3 et certificats SSL automatiques\n"
                "Sauvegardes quotidiennes chiffrées hors site avec politique de rétention\n"
                "Mise en place de déploiements continus sans interruption (zero-downtime)\n"
                "Sécurisation avancée du serveur (Pare-feu UFW, Fail2ban, accès SSH par clés)\n"
                "Tableau de bord de télémétrie des performances et notifications d'anomalies\n"
                "Manuel de reprise d'activité documenté pour restauration rapide en cas de sinistre"
            ),
            'deliverables_ar': (
                "ملفات حاويات دوكر (Docker) محكمة ومبنية على مراحل متعددة\n"
                "مسار نشر آلي متكامل عبر GitHub Actions يختصر ساعات العمل اليدوي\n"
                "تهيئة خادم Nginx السريع مع دعم HTTP/2 وشهادات التشفير التلقائية SSL\n"
                "نظام نسخ احتياطي يومي مشفر يتم حفظه خارج السيرفر لحماية البيانات\n"
                "آلية نشر وتحديث للبرمجيات دون توقف الخدمة عن الزوار نهائياً\n"
                "تحصين شامل للسيرفر وجدار الحماية UFW ومنع الهجمات عبر Fail2ban\n"
                "نظام مراقبة ذكي يرصد استهلاك الموارد ويرسل تنبيهات فورية\n"
                "دليل تشغيلي متكامل لخطوات استعادة النظام والبيانات في حالات الطوارئ"
            ),
            'target_audience_en': (
                "• Growing Web & Mobile Businesses: Platforms outgrowing shared hosting and crashing under user spikes.\n"
                "• Software Teams Lacking Dedicated DevOps: Engineering teams spending too much developer time manually configuring servers.\n"
                "• E-Commerce Stores & Transactional Platforms: High-value sites where downtime directly causes revenue loss.\n"
                "• Moroccan & European Enterprises: Organizations requiring strict GDPR and Moroccan CNDP data residency compliance."
            ),
            'target_audience_fr': (
                "• Entreprises digitales en forte croissance : Plateformes limitées par les hébergements classiques subissant des ralentissements.\n"
                "• Équipes techniques sans ressource DevOps dédiée : Développeurs perdant un temps précieux en maintenance de serveurs.\n"
                "• Boutiques e-commerce et plateformes transactionnelles : Sites où la moindre minute d'interruption impacte directement le chiffre d'affaires.\n"
                "• Sociétés marocaines et européennes : Organisations soumises aux exigences strictes de protection des données (RGPD / CNDP)."
            ),
            'target_audience_ar': (
                "• الشركات الرقمية سريعة النمو: المنصات التي تجاوزت حدود الاستضافات العادية وتعاني من بطء في أوقات الذروة.\n"
                "• الفرق البرمجية التي تفتقر لخبير DevOps: المطورون الذين يضيعون أوقاتهم الثمينة في ضبط السيرفرات يدوياً.\n"
                "• المتاجر الإلكترونية ومنصات الدفع: المواقع الحساسة التي يكلفها كل دقيقة توقف خسائر مادية مباشرة.\n"
                "• الشركات المغربية والأوروبية: المؤسسات الملتزمة بمعايير حماية البيانات والخصوصية الصارمة (CNDP / GDPR)."
            ),
            'process_steps_en': (
                "Step 1: Architecture Review & Threat Audit (Week 1) — Resource profiling, security baseline, and tooling choice.\n"
                "Step 2: Dockerization & Environment Parity (Weeks 1–2) — Containerizing backend, database, and caching tiers.\n"
                "Step 3: CI/CD Pipeline Automation (Weeks 2–3) — Automated testing and push-to-deploy workflows.\n"
                "Step 4: Backup Automation & Failure Drills (Week 4) — Testing automated restoration from encrypted backups.\n"
                "Step 5: Handover, Telemetry & SLA Retainer — Provisioning monitoring dashboards and continuous maintenance."
            ),
            'process_steps_fr': (
                "Étape 1 : Diagnostic & Cadrage (Semaine 1) — Évaluation des charges, besoins en bande passante et sécurité.\n"
                "Étape 2 : Conteneurisation & Environnements (Semaines 1–2) — Création des conteneurs Docker pour chaque service.\n"
                "Étape 3 : Automatisation CI/CD (Semaines 2–3) — Mise en place du déploiement continu via GitHub Actions.\n"
                "Étape 4 : Sauvegardes & Tests de Résilience (Semaine 4) — Exercices pratiques de restauration de données.\n"
                "Étape 5 : Mise en Production & Support — Configuration des alertes et contrat d'infogérance proactive."
            ),
            'process_steps_ar': (
                "المرحلة 1: التدقيق وتحليل الاحتياجات (الأسبوع 1) — فحص حجم الزيارات والموارد اللازمة وتحديد معايير الحماية.\n"
                "المرحلة 2: إعداد حاويات دوكر (الأسابيع 1-2) — عزل قواعد البيانات وتطبيقات الويب في حاويات مستقلة.\n"
                "المرحلة 3: أتمتة خطوط النشر CI/CD (الأسابيع 2-3) — بناء مسارات التحديث التلقائي الفوري للكود.\n"
                "المرحلة 4: النسخ الاحتياطي واختبار الطوارئ (الأسبوع 4) — تجربة استرجاع قواعد البيانات للتأكد من سلامتها.\n"
                "المرحلة 5: التشغيل النهائي والدعم (الأسبوع 5+) — تفعيل شاشات المراقبة وتقديم الصيانة السحابية المستمرة."
            ),
            'pricing_guidance_en': (
                "Cloud infrastructure provisioning, containerization, and automated CI/CD pipeline setups range from $1,200 to $5,000 (approx. 12,000 to 50,000 MAD) for initial implementation, with optional ongoing DevOps maintenance retainers. "
                "TODO(owner): Confirm final DevOps pricing tiers and cloud retainer agreements."
            ),
            'pricing_guidance_fr': (
                "La mise en place d'une infrastructure cloud, conteneurisation et pipeline CI/CD se situe entre 12 000 et 50 000 MAD pour la configuration initiale, avec option de contrat d'infogérance mensuel. "
                "TODO(owner): Confirmer les forfaits d'infogérance et de déploiement cloud."
            ),
            'pricing_guidance_ar': (
                "تبدأ خدمات تهيئة الخوادم السحابية والحاويات وأتمتة النشر من 12,000 إلى 50,000 درهم مغربي للتهيئة الأولية، مع عقود دعم وإدارة شهرية اختيارية. "
                "TODO(owner): تأكيد الأسعار الرسمية لخدمات الحوسبة السحابية والديف أوبس."
            ),
            'technologies': 'Docker, Docker Compose, AWS, Linux, Nginx, GitHub Actions, PostgreSQL, Redis, Terraform',
            'timeline': '2 — 6 Weeks',
            'faqs': [
                (
                    "Can you host our application on European servers for GDPR compliance?",
                    "Pouvez-vous héberger notre application sur des serveurs européens pour la conformité RGPD ?",
                    "هل يمكنكم استضافة تطبيقاتنا على خوادم أوروبية لضمان الامتثال لقوانين حماية البيانات (GDPR)؟",
                    "Yes. We frequently deploy client applications to enterprise datacenters in Germany, France, and Ireland (AWS and Hetzner), ensuring full GDPR compliance, ultra-low latency to Europe, and strict data sovereignty.",
                    "Oui. Nous déployons régulièrement les applications de nos clients sur des datacenters en Allemagne, en France ou en Irlande (AWS et Hetzner), garantissant une conformité RGPD totale et une latence minime.",
                    "نعم. نقوم بانتظام بنشر واستضافة تطبيقات عملائنا في مراكز بيانات أوروبية معتمدة (في ألمانيا وفرنسا وأيرلندا عبر AWS و Hetzner) لضمان الامتثال التام لقوانين GDPR وسرعة استجابة فائقة."
                ),
            ]
        }
    }

    for slug, data in services_data.items():
        try:
            service = Service.objects.get(slug=slug)
        except Service.DoesNotExist:
            continue

        service.title_en = data['title_en']
        service.title_fr = data['title_fr']
        service.title_ar = data['title_ar']
        service.subtitle_en = data['subtitle_en']
        service.subtitle_fr = data['subtitle_fr']
        service.subtitle_ar = data['subtitle_ar']
        service.description_en = data['description_en']
        service.description_fr = data['description_fr']
        service.description_ar = data['description_ar']
        service.methodology_en = data['methodology_en']
        service.methodology_fr = data['methodology_fr']
        service.methodology_ar = data['methodology_ar']
        service.deliverables_en = data['deliverables_en']
        service.deliverables_fr = data['deliverables_fr']
        service.deliverables_ar = data['deliverables_ar']
        service.target_audience_en = data['target_audience_en']
        service.target_audience_fr = data['target_audience_fr']
        service.target_audience_ar = data['target_audience_ar']
        service.process_steps_en = data['process_steps_en']
        service.process_steps_fr = data['process_steps_fr']
        service.process_steps_ar = data['process_steps_ar']
        service.pricing_guidance_en = data['pricing_guidance_en']
        service.pricing_guidance_fr = data['pricing_guidance_fr']
        service.pricing_guidance_ar = data['pricing_guidance_ar']
        service.technologies = data['technologies']
        service.timeline = data['timeline']
        service.save()

        # Populate service-specific FAQs
        for q_en, q_fr, q_ar, a_en, a_fr, a_ar in data.get('faqs', []):
            faq, _ = FAQ.objects.get_or_create(
                question_en=q_en,
                defaults={
                    'service': service,
                    'section': 'services',
                    'question_fr': q_fr,
                    'question_ar': q_ar,
                    'answer_en': a_en,
                    'answer_fr': a_fr,
                    'answer_ar': a_ar,
                    'is_active': True,
                }
            )
            if faq.service != service:
                faq.service = service
                faq.question_fr = q_fr
                faq.question_ar = q_ar
                faq.answer_en = a_en
                faq.answer_fr = a_fr
                faq.answer_ar = a_ar
                faq.save()

def reverse_service_deep_content(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_faq_service_service_pricing_guidance_ar_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_service_deep_content, reverse_service_deep_content),
    ]
