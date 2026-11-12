from django.db import migrations

def expand_city_service_content(apps, schema_editor):
    CityServicePage = apps.get_model('core', 'CityServicePage')

    city_data = {
        'web-development-tangier': {
            'h1_en': 'Web Development Agency in Tangier, Morocco',
            'h1_fr': 'Agence de Développement Web à Tanger, Maroc',
            'h1_ar': 'وكالة تطوير مواقع وتطبيقات الويب في طنجة، المغرب',
            'intro_en': (
                "Based directly in Tangier, getNexiro delivers custom web application development and scalable software platforms for businesses across the Tangier-Tétouan-Al Hoceima region and international partners in Europe. "
                "From our studio near the commercial center of Tangier, we engineer fast, secure, and multilingual web platforms tailored to the Mediterranean economy."
            ),
            'intro_fr': (
                "Directement implantée à Tanger, getNexiro conçoit des applications web sur mesure et des plateformes logicielles évolutives pour les entreprises de la région Tanger-Tétouan-Al Hoceïma et les partenaires européens. "
                "Depuis notre studio à Tanger, nous développons des solutions numériques rapides, sécurisées et multilingues parfaitement alignées sur l'économie euro-méditerranéenne."
            ),
            'intro_ar': (
                "انطلاقاً من موقعنا المباشر في مدينة طنجة، تقدم جيت نكسيرو (getNexiro) خدمات تطوير مواقع وتطبيقات الويب المتطورة والحلول البرمجية القابلة للتوسع للشركات في جهة طنجة تطوان الحسيمة وشركائنا في أوروبا. "
                "من استوديونا بالقرب من المركز التجاري لطنجة، نهندس منصات ويب سريعة، آمنة ومتعددة اللغات متوافقة تماماً مع متطلبات الاقتصاد المتوسطي."
            ),
            'body_en': (
                "<h3>Engineering Web Systems for Tangier's Thriving Economic Corridor</h3>"
                "<p>Tangier is currently Morocco's premier economic powerhouse outside Casablanca, driven by the colossal Tanger Med Port—the leading container terminal on both the Mediterranean and the African continent—alongside the Tangier Free Zone (TFZ) and Tangier Automotive City (TAC). For industrial operators, freight forwarders, logistics coordinators, and commercial enterprises operating within this bustling ecosystem, off-the-shelf software and slow template websites fail to address the complex requirements of cross-border operations.</p>"
                "<p>getNexiro builds bespoke web applications designed specifically to meet the high-throughput demands of Tangier companies. We specialize in developing custom operations dashboards, multilingual client booking portals, supply chain tracking interfaces, and secure B2B transaction hubs. Our engineering stack relies on Python with Django for robust, enterprise-grade backends, PostgreSQL for relational data integrity, and Next.js / React for sub-second, highly responsive user experiences.</p>"
                "<h3>Why Local Presence in Tangier Matters for Your Engineering Project</h3>"
                "<p>While software runs in the cloud, effective technical collaboration thrives on geographic proximity. Because our core engineering studio is located right here in Tangier, we provide local clients with direct on-site architectural workshops, face-to-face sprint planning, and same-day support without time zone friction or communication delays. Whether you manage manufacturing operations in Gzenaya, shipping logistics at Tanger Med, or private healthcare clinics in the city center, our engineers can sit down with your team to model requirements in person.</p>"
                "<p>Simultaneously, our strategic Tangier location gives European clients seeking nearshore software development teams a decisive advantage: perfect GMT+1 timezone alignment, fluent trilingual communication (English, French, Arabic), and European engineering standards delivered at competitive nearshore rates.</p>"
                "<h3>Comprehensive Capabilities Delivered from Tangier</h3>"
                "<p>Every web system engineered by our Tangier team includes comprehensive full-cycle delivery:</p>"
                "<ul>"
                "<li><strong>Custom Database Modeling:</strong> Clean, normalized PostgreSQL schemas designed for complex Moroccan tax rules, currency conversions (MAD, EUR, USD), and multi-warehouse stock management.</li>"
                "<li><strong>Native Multilingual Localization:</strong> Complete trilingual parity across French, English, and Arabic, featuring dedicated bidirectional RTL layout styling and natural phrasing.</li>"
                "<li><strong>Enterprise Security & Compliance:</strong> Strict Moroccan CNDP data privacy compliance, HTTPS/TLS encryption, and automated offsite encrypted backups.</li>"
                "<li><strong>High-Speed Hosting:</strong> Optimized cloud server configurations providing sub-100ms response times for visitors across Morocco and Western Europe.</li>"
                "</ul>"
            ),
            'body_fr': (
                "<h3>L'Ingénierie Web au Cœur du Pôle Économique de Tanger</h3>"
                "<p>Tanger s'impose aujourd'hui comme le deuxième pôle économique du Maroc, porté par la dynamique exceptionnelle de Tanger Med—premier port à conteneurs de Méditerranée et d'Afrique—ainsi que par la Zone Franche de Tanger (TFZ) et Tanger Automotive City (TAC). Pour les industriels, transitaires, coordinateurs logistiques et sociétés de services de la région, les sites internet génériques et modèles préconçus ne répondent plus aux exigences rigoureuses du commerce moderne.</p>"
                "<p>getNexiro conçoit des applications web sur mesure adaptées aux besoins de performance des entreprises tangéroises. Nous développons des portails de gestion opérationnelle, des interfaces de suivi logistique, des plateformes médicales sécurisées et des solutions de commerce B2B fluides. Notre socle technique s'appuie sur Python/Django pour un backend robuste, PostgreSQL pour l'intégrité des données critiques, et Next.js/React pour des interfaces ultra-rapides et responsives.</p>"
                "<h3>L'Avantage d'une Équipe d'Ingénierie Présente à Tanger</h3>"
                "<p>Bien que le code soit hébergé dans le cloud, la réussite d'un projet technologique repose sur la proximité humaine. Grâce à l'implantation de notre studio à Tanger, nos clients locaux bénéficient d'ateliers de cadrage en présentiel, de réunions de sprint régulières et d'un support réactif sans décalage horaire ni barrière linguistique. Que vous dirigiez une usine à Gzenaya, une agence maritime ou une clinique au centre-ville, nous intervenons directement dans vos locaux.</p>"
                "<p>Pour nos clients européens, notre présence à Tanger représente un atout nearshore stratégique : un fuseau horaire identique (GMT+1), une maîtrise parfaite du français et de l'anglais, et des standards de développement européens à des tarifs hautement compétitifs.</p>"
                "<h3>Nos Engagements Techniques à Tanger</h3>"
                "<p>Chaque plateforme conçue par notre studio de Tanger intègre des exigences de qualité strictes :</p>"
                "<ul>"
                "<li><strong>Modélisation de données sur mesure :</strong> Bases PostgreSQL adaptées à la facturation marocaine, au multidevise (MAD/EUR/USD) et à la gestion multi-sites.</li>"
                "<li><strong>Multilinguisme natif :</strong> Parité parfaite français, anglais et arabe avec mise en page RTL soignée et ergonomique.</li>"
                "<li><strong>Conformité CNDP & Sécurité :</strong> Respect des normes de protection des données personnelles, chiffrement TLS et sauvegardes quotidiennes chiffrées.</li>"
                "<li><strong>Performance d'hébergement :</strong> Temps de réponse inférieurs à 100ms pour les utilisateurs au Maroc et en Europe.</li>"
                "</ul>"
            ),
            'body_ar': (
                "<h3>تطوير الأنظمة البرمجية ومواقع الويب لمواكبة النهضة الاقتصادية بطنجة</h3>"
                "<p>تعد مدينة طنجة اليوم القطب الاقتصادي والصناعي الأبرز في المملكة المغربية، بفضل ميناء طنجة المتوسط الرائد إفريقياً ومتوسطياً، إلى جانب المنطقة الحرة للتصدير (TFZ) ومدينة صناعة السيارات (TAC). بالنسبة للمؤسسات الصناعية، شركات اللوجستيك والشحن، والأنشطة التجارية في هذه البيئة السريعة، لم تعد القوالب الجاهزة تلبي الاحتياجات المتقدمة لإدارة العمليات اليومية.</p>"
                "<p>تبني جيت نكسيرو (getNexiro) تطبيقات ومواقع ويب مخصصة تواكب المعايير العالية للشركات في طنجة. نتخصص في برمجة لوحات التحكم الإدارية، بوابات إدارة حجوزات المرضى والتحاليل الطبية، منصات تتبع الشحنات، ومنظومات التجارة الإلكترونية بين الشركات (B2B). نعتمد على أحدث التقنيات مثل بايثون ودجانغو للخوادم الخلفية، وقواعد بيانات بوستجريسيل، ورياكت/نكست لتجربة تصفح فورية لا تتجاوز أجزاء من الثانية.</p>"
                "<h3>أهمية وجود شريك تقني مباشر ومحلي في طنجة</h3>"
                "<p>رغم أن الأنظمة السحابية تعمل عبر الإنترنت، إلا أن التعاون المثمر يتطلب قرباً وتواصلاً مباشراً. وبفضل تواجد مقرنا بطنجة، يستفيد عملاؤنا المحليون من ورشات عمل تخطيطية حضورية، واجتماعات دورية، واستجابة سريعة دون أي عوائق في التوقيت أو اللغة. سواء كنتم تديرون منشأة صناعية في كزناية، أو نشاطاً لوجستياً بميناء طنجة المتوسط، أو مركزاً طبياً وسط المدينة، فإن مهندسينا على تواصل مباشر معكم.</p>"
                "<p>وفي الوقت ذاته، يوفر موقع طنجة لشركائنا في أوروبا ميزة Nearshore استثنائية: توافق كامل في التوقيت (GMT+1)، تواصل سلس باللغات الإنجليزية والفرنسية والعربية، ومعايير جودة أوروبية بتكلفة استثمارية تنافسية.</p>"
                "<h3>التزاماتنا الهندسية في طنجة</h3>"
                "<p>يتضمن كل مشروع ننجزه في طنجة معايير تسليم شاملة:</p>"
                "<ul>"
                "<li><strong>هندسة قواعد بيانات دقيقة:</strong> متوافقة مع متطلبات الفوترة المغربية وتعدد العملات (الدرهم، اليورو، الدولار).</li>"
                "<li><strong>دعم لغوي أصيل وثلاثي:</strong> دعم كامل للعربية (RTL)، الفرنسية، والإنجليزية بصياغة متقنة وتصميم مريح للعين.</li>"
                "<li><strong>حماية البيانات والامتثال:</strong> توافق كامل مع معايير اللجنة الوطنية لمراقبة حماية المعطيات ذات الطابع الشخصي (CNDP).</li>"
                "<li><strong>سرعة استجابة فائقة:</strong> استضافة سحابية مدارة تحقق سرعة تحميل أقل من 100ms للزوار في المغرب وأوروبا.</li>"
                "</ul>"
            ),
            'why_choose_us_en': (
                "<ul>"
                "<li><strong>Local Studio with European Standards:</strong> Direct face-to-face meetings in Tangier combined with nearshore engineering rigor.</li>"
                "<li><strong>Deep Regional Domain Knowledge:</strong> Proven experience with Tanger Med logistics workflows, industrial zones, and local business regulations.</li>"
                "<li><strong>True Trilingual Architecture:</strong> Seamless support for French, English, and natural Arabic RTL interfaces.</li>"
                "<li><strong>Zero-Disruption Migration:</strong> Smooth transition from legacy tools with zero operational downtime for your business.</li>"
                "</ul>"
            ),
            'why_choose_us_fr': (
                "<ul>"
                "<li><strong>Studio local aux standards internationaux :</strong> Rencontres directes à Tanger et rigueur méthodologique d'ingénierie.</li>"
                "<li><strong>Expertise de l'écosystème régional :</strong> Maîtrise des enjeux logistiques de Tanger Med, des zones franches et du tissu économique local.</li>"
                "<li><strong>Trilinguisme naturel :</strong> Conception native en français, anglais et arabe avec mise en page RTL irréprochable.</li>"
                "<li><strong>Continuité d'activité garantie :</strong> Migration sans interruption de service pour vos opérations quotidiennes.</li>"
                "</ul>"
            ),
            'why_choose_us_ar': (
                "<ul>"
                "<li><strong>استوديو محلي بمعايير عالمية:</strong> لقاءات مباشرة في طنجة مع انضباط هندسي أوروبي.</li>"
                "<li><strong>فهم عميق للاقتصاد المحلي:</strong> خبرة ميدانية في لوجستيك طنجة المتوسط والمناطق الحرة والقطاع الصحي.</li>"
                "<li><strong>دعم كامل للغات الثلاث:</strong> واجهات عربية وفرنسية وإنجليزية أصلية مع اتجاه RTL طبيعي.</li>"
                "<li><strong>استمرارية الأعمال دون انقطاع:</strong> نقل الأنظمة القديمة بسلاسة دون التأثير على سير العمليات.</li>"
                "</ul>"
            ),
            'industries_en': 'Automotive & Aeronautics, Maritime Logistics, Healthcare & Clinics, Mediterranean Trade, Tourism & Hospitality',
            'industries_fr': 'Automobile & Aéronautique, Logistique Maritime, Santé & Cliniques, Commerce Méditerranéen, Tourisme & Hôtellerie',
            'industries_ar': 'صناعة السيارات والطيران، اللوجستيك والشحن البحري، الصحة والمصحات، التجارة الدولية، السياحة والفندقة',
        },
        'web-development-tetouan': {
            'h1_en': 'Web Development in Tétouan, Morocco',
            'h1_fr': 'Développement Web à Tétouan, Maroc',
            'h1_ar': 'تطوير مواقع وتطبيقات الويب في تطوان، المغرب',
            'intro_en': (
                "Serving growing enterprises, tourism brands, and tech ventures across Tétouan, Martil, and Cabo Negro from our regional studio in Tangier. "
                "We engineer high-performance web systems, hospitality booking engines, and business portals backed by dedicated local support."
            ),
            'intro_fr': (
                "Au service des entreprises, acteurs du tourisme et initiatives technologiques de Tétouan, Martil et Cabo Negro depuis notre studio régional à Tanger. "
                "Nous développons des plateformes web performantes, moteurs de réservation hôteliers et portails d'entreprise avec un accompagnement de proximité."
            ),
            'intro_ar': (
                "نخدم الشركات الناشئة، المؤسسات السياحية والتجارية في تطوان، مرتيل، وكابو نيغرو انطلاقاً من استوديونا الإقليمي بطنجة. "
                "نطور منصات ويب سريعة، ومحركات حجز فندقي، وبوابات أعمال متقدمة بدعم تقني مباشر."
            ),
            'body_en': (
                "<h3>Digital Engineering for Tétouan's Expanding Business Ecosystem</h3>"
                "<p>Tétouan and the coastal corridor connecting Martil, M'diq, and Cabo Negro represent one of Morocco's most dynamic regional economies, marked by the Tétouan Shore offshoring park, thriving hospitality and luxury tourism, construction and building material distribution, and high-value agricultural initiatives. As regional companies scale beyond local markets, having a high-performing digital platform becomes the single most critical asset for growth.</p>"
                "<p>getNexiro provides Tétouan businesses with top-tier software engineering without the overhead or impersonal treatment of mega-agencies. Our Tangier headquarters is situated just 45 minutes away via the A4 highway, allowing our engineering team to provide Tétouan clients with the perfect balance: deep on-site availability for architecture workshops and strategy sessions, combined with cutting-edge cloud software engineering.</p>"
                "<h3>Tailored Solutions for Tétouan's Leading Sectors</h3>"
                "<p>We design and engineer bespoke web solutions addressing Tétouan's distinct commercial landscape:</p>"
                "<ul>"
                "<li><strong>Luxury Tourism & Hospitality Portals:</strong> Custom reservation engines for boutique hotels, resorts, and vacation rentals in Cabo Negro and Tamuda Bay, bypassing high booking platform commissions with direct payment integration (CMI, Stripe).</li>"
                "<li><strong>Tétouan Shore Tech Ventures:</strong> Scalable web application backends and client interfaces for tech scaleups and outsourcing teams requiring reliable Python/Django and React architectures.</li>"
                "<li><strong>Regional Commercial Distributors:</strong> Wholesale catalog portals, inventory tracking systems, and dealer ordering workflows for construction, building supplies, and agro-food distributors.</li>"
                "<li><strong>Medical & Professional Services:</strong> Specialized clinic management portals with online appointment scheduling and patient result access.</li>"
                "</ul>"
                "<h3>Nearshore Reliability Backed by Tangier Engineering Hub</h3>"
                "<p>Working with getNexiro means Tétouan organizations don't have to look to Casablanca or offshore consultancies for enterprise engineering. Every solution we build includes clean relational database architecture, rigorous security protocols, full multilingual localization (English, French, and natural Arabic RTL), and proactive maintenance retainers ensuring 99.98% uptime.</p>"
            ),
            'body_fr': (
                "<h3>L'Ingénierie Numérique pour l'Écosystème Entreprise de Tétouan</h3>"
                "<p>Tétouan et le littoral de Martil, M'diq et Cabo Negro constituent une zone économique en plein essor, dynamisée par le parc Tétouan Shore, une hôtellerie de prestige, le négoce de matériaux et l'agroalimentaire. Pour les entreprises de la région, disposer d'une vitrine numérique performante et d'outils web sur mesure est devenu le levier fondamental de développement commercial.</p>"
                "<p>getNexiro apporte aux entreprises de Tétouan une ingénierie logicielle d'élite avec un accompagnement de proximité. Notre studio de Tanger, situé à seulement 45 minutes via l'autoroute A4, garantit une disponibilité physique immédiate pour vos réunions de travail, combinée à une rigueur technologique de haut niveau.</p>"
                "<h3>Solutions Spécifiques pour les Filières Clés de Tétouan</h3>"
                "<p>Nous concevons des plateformes web adaptées au tissu économique tétouanais :</p>"
                "<ul>"
                "<li><strong>Hôtellerie et Tourisme Haut de Gamme :</strong> Moteurs de réservation directs pour établissements hôteliers et résidences de Tamuda Bay et Cabo Negro, supprimant les commissions intermédiaires grâce aux paiements sécurisés CMI/Stripe.</li>"
                "<li><strong>Entreprises de Tétouan Shore :</strong> Backends d'applications évolutifs et interfaces modernes pour les sociétés de services informatiques et startups locales.</li>"
                "<li><strong>Négoce et Distribution :</strong> Portails de commandes B2B, catalogues produits et suivi des stocks pour les grossistes en matériaux et agroalimentaire.</li>"
                "<li><strong>Cabinets et Cliniques :</strong> Espaces patients intuitifs pour la prise de rendez-vous et la consultation sécurisée de dossiers médicaux.</li>"
                "</ul>"
            ),
            'body_ar': (
                "<h3>الهندسة الرقمية لخدمة النسيج الاقتصادي المتنامي في تطوان</h3>"
                "<p>تشهد مدينة تطوان والشريط الساحلي الممتد نحو مرتيل والمضيق وكابو نيغرو نمواً اقتصادياً لافتاً، مدعوماً بحظيرة تطوان شور (Tétouan Shore)، وقطاع السياحة الفندقية الراقية، وتجارة مواد البناء، والصناعات الغذائية. ومع توسع الأنشطة التجارية في المنطقة، أصبحت الحاجة ملحة لمنصات رقمية متطورة تفتح آفاقاً أوسع للأعمال.</p>"
                "<p>تقدم جيت نكسيرو (getNexiro) للمؤسسات في تطوان حلولاً برمجية متقدمة بأعلى المعايير، مع ميزة القرب الجغرافي؛ حيث يبعد مقرنا في طنجة 45 دقيقة فقط عبر الطريق السيار A4، مما يتيح لقاءات عمل مباشرة وتنسيقاً وثيقاً مع فريق التطوير.</p>"
                "<h3>حلول مخصصة للقطاعات الرئيسية في تطوان</h3>"
                "<ul>"
                "<li><strong>السياحة والفندقة الراقية:</strong> محركات حجز مخصصة للمنتجعات والفنادق في كابو نيغرو وخليج تمودا، مع ربط مباشر ببوابات الدفع الإلكتروني (CMI) لتفادي عمولات الوسطاء.</li>"
                "<li><strong>شركات تكنولوجيا المعلومات بتطوان شور:</strong> بناء خوادم خلفية متينة وواجهات سريعة للشركات الناشئة ومنصات التعهيد.</li>"
                "<li><strong>تجارة الجملة والتوزيع:</strong> بوابات إلكترونية للطلبيات بين الشركات (B2B) ومتابعة المخازن لشركات البناء والمواد الغذائية.</li>"
                "<li><strong>القطاع الصحي والمصحات:</strong> بوابات مخصصة لحجز مواعيد المرضى وعرض الفحوصات والتحاليل في بيئة رقمية آمنة.</li>"
                "</ul>"
            ),
            'why_choose_us_en': (
                "<ul>"
                "<li><strong>45 Minutes Away via A4:</strong> In-person meetings in Tétouan combined with full engineering horsepower in Tangier.</li>"
                "<li><strong>Hospitality & Tourism Expertise:</strong> Custom commission-free booking engines with CMI and international card processing.</li>"
                "<li><strong>Bespoke Trilingual Architecture:</strong> Fluent English, French, and native Arabic RTL tailored to local and international guests.</li>"
                "<li><strong>Long-Term Partnership:</strong> Dedicated maintenance, security updates, and performance monitoring.</li>"
                "</ul>"
            ),
            'why_choose_us_fr': (
                "<ul>"
                "<li><strong>À 45 minutes via l'A4 :</strong> Réunions en présentiel à Tétouan et puissance d'ingénierie de notre pôle de Tanger.</li>"
                "<li><strong>Expertise hôtelière reconnue :</strong> Moteurs de réservation sans commission avec intégration CMI et cartes internationales.</li>"
                "<li><strong>Conception trilingue soignée :</strong> Français, anglais et arabe RTL adaptés aux clientèles locales et étrangères.</li>"
                "<li><strong>Support pérenne :</strong> Maintenance proactive, sauvegardes continues et optimisation des performances.</li>"
                "</ul>"
            ),
            'why_choose_us_ar': (
                "<ul>"
                "<li><strong>على بعد 45 دقيقة فقط:</strong> اجتماعات حضورية سهلة في تطوان مع قوة التطوير البرمجي من طنجة.</li>"
                "<li><strong>خبرة في القطاع السياحي:</strong> محركات حجز مستقلة بدون عمولات مع الدفع المباشر بالبطاقات المغربية والدولية.</li>"
                "<li><strong>إتقان لغوي ثلاثي:</strong> العربية، الفرنسية، والإنجليزية بتنسيق مثالي يخدم كافة فئات الزبائن.</li>"
                "<li><strong>دعم وصيانة مستمرة:</strong> مواكبة تقنية وتحديثات أمان مستمرة لضمان استقرار المواقع على مدار الساعة.</li>"
                "</ul>"
            ),
            'industries_en': 'Hospitality & Luxury Resorts, Real Estate, Offshoring & IT, Building Materials, Regional Retail',
            'industries_fr': 'Hôtellerie & Resorts, Immobilier, Offshoring & IT, Matériaux de Construction, Distribution Régionale',
            'industries_ar': 'الفندقة والمنتجعات، العقارات، تكنولوجيا المعلومات، مواد البناء، التجارة الإقليمية',
        },
        'web-development-fes': {
            'h1_en': 'Web Development in Fès, Morocco',
            'h1_fr': 'Développement Web à Fès, Maroc',
            'h1_ar': 'تطوير مواقع وتطبيقات الويب في فاس، المغرب',
            'intro_en': (
                "Empowering enterprises, exporters, and technology ventures across Fès and the Fès-Meknès region with high-performance web development. "
                "Delivered by our senior engineering studio in Tangier with seamless remote collaboration and Al Boraq high-speed connectivity."
            ),
            'intro_fr': (
                "Au service des entreprises, exportateurs et acteurs technologiques de Fès et de sa région avec des solutions web haute performance. "
                "Réalisées par notre studio d'ingénierie à Tanger avec un suivi à distance fluide et des liaisons rapides via le réseau ferroviaire."
            ),
            'intro_ar': (
                "ندعم المؤسسات والشركات المصدرة والأنشطة الرقمية في فاس وجهة فاس مكناس بحلول برمجية وتطوير ويب عالي الأداء. "
                "نقدم خدماتنا من استوديونا الهندسي بطنجة مع إدارة مشاريع مرنة وتواصل مستمر."
            ),
            'body_en': (
                "<h3>Modern Software Engineering for Fès: Bridging Tradition and High Tech</h3>"
                "<p>Fès holds a distinguished position in Morocco as a historic intellectual and commercial capital that is rapidly modernizing. With the strategic expansion of Fès Shore offshoring park, prestigious higher education and engineering institutions (such as Euromed University and Sidi Mohamed Ben Abdellah), an internationally recognized craft and leather export sector, and an expanding medical and wellness tourism industry, businesses in Fès require modern, sophisticated digital systems to compete both nationally and globally.</p>"
                "<p>getNexiro provides forward-thinking Fès companies with enterprise-grade web development designed to accelerate operational velocity. Operating from our central studio in Tangier, we deliver complete technical solutions via disciplined agile sprints, weekly interactive video demonstrations, transparent project dashboards, and on-site visits via Morocco's high-speed rail network whenever in-person alignment is needed.</p>"
                "<h3>High-Impact Solutions for Fès Enterprises</h3>"
                "<p>We partner with Fès organizations across key strategic verticals:</p>"
                "<ul>"
                "<li><strong>International Export & Artisan E-Commerce:</strong> Premium, multilingual e-commerce platforms showcasing Moroccan craftsmanship, leather, textiles, and ceramics to international buyers in Europe and North America, equipped with multi-currency checkout, DHL/FedEx logistics integration, and high-conversion UX.</li>"
                "<li><strong>Fès Shore Offshoring Ventures:</strong> High-throughput backend systems, internal tools, and customer portals developed with Python/Django and modern JavaScript frameworks.</li>"
                "<li><strong>Healthcare & Specialized Medical Clinics:</strong> Secure patient appointment portals and laboratory results systems complying with Moroccan privacy standards.</li>"
                "<li><strong>Educational & Training Platforms:</strong> Custom learning management systems (LMS) and student intake portals for regional educational institutions.</li>"
                "</ul>"
                "<h3>Enterprise Quality Without Geographic Limitations</h3>"
                "<p>By partnering with getNexiro in Tangier, Fès enterprises gain direct access to senior software architects specializing in Django, Next.js, and cloud infrastructure. We ensure every platform is built with sub-second response times, native multilingual translation (Arabic, French, English), and robust database modeling that scales effortlessly with your business growth.</p>"
            ),
            'body_fr': (
                "<h3>L'Ingénierie Logicielle pour Fès : Entre Héritage et Innovation Technologique</h3>"
                "<p>Capitale historique et intellectuelle du Maroc, Fès connaît une modernisation économique soutenue. Grâce au parc d'offshoring Fès Shore, à ses universités réputées, à ses filières d'exportation artisanale et textile de renommée mondiale et à son pôle médical de référence, les entreprises fassies ont besoin d'outils numériques performants pour affirmer leur compétitivité.</p>"
                "<p>getNexiro accompagne les entreprises de Fès avec un développement web haut de gamme. Depuis notre studio à Tanger, nous menons les projets selon une méthode agile rigoureuse : démonstrations de sprint hebdomadaires en visioconférence, tableau de bord transparent et déplacements réguliers en présentiel grâce aux liaisons rapides Al Boraq.</p>"
                "<h3>Solutions Digitales Adaptées aux Entreprises de Fès</h3>"
                "<p>Nous intervenons sur les secteurs stratégiques de la région fassie :</p>"
                "<ul>"
                "<li><strong>E-Commerce d'Export & Artisanat d'Art :</strong> Plateformes e-commerce premium pour l'exportation du cuir, textile et céramique vers l'Europe et l'Amérique, avec paiement multidevise et suivi d'expédition international.</li>"
                "<li><strong>Sociétés de Fès Shore :</strong> Architectures backend robustes sous Python/Django et API microservices pour les acteurs des nouvelles technologies.</li>"
                "<li><strong>Cliniques et Laboratoires Médicaux :</strong> Espaces patients conformes aux exigences de confidentialité CNDP pour la prise de rendez-vous et le partage des bilans.</li>"
                "<li><strong>Établissements d'Enseignement :</strong> Portails de formation et d'inscription sur mesure pour les écoles et instituts de la région.</li>"
                "</ul>"
            ),
            'body_ar': (
                "<h3>هندسة البرمجيات الحديثة في فاس: الجمع بين الأصالة والتقنية العالية</h3>"
                "<p>تحظى العاصمة العلمية والتاريخية فاس بمكانة استراتيجية تتجدد باستمرار في الاقتصاد المغربي. ومع التوسع المتواصل لحظيرة فاس شور (Fès Shore)، وتواجد جامعات ومعاهد رائدة، وازدهار قطاع تصدير الصناعات التقليدية والنسيج والجلد نحو العالم، إلى جانب المراكز الطبية المتخصصة، تحتاج شركات فاس إلى حلول برمجية متطورة تواكب الطموحات الكبرى.</p>"
                "<p>توفر جيت نكسيرو (getNexiro) للشركات في فاس خدمات تطوير ويب متقدمة بالاعتماد على منهجية عمل رقمية رشيقة. ومن خلال استوديونا في طنجة، ندير المشاريع بكفاءة عبر عروض أسبوعية مرئية، وتنسيق تقني مستمر، وزيارات حضورية ميسرة عبر شبكة القطار فائق السرعة عند الحاجة.</p>"
                "<h3>حلول برمجية موجهة لقطاعات الأعمال في فاس</h3>"
                "<ul>"
                "<li><strong>التجارة الإلكترونية والتصدير الدولي:</strong> متاجر إلكترونية راقية لتسويق المنتجات التقليدية والجلدية للخارج مع الدفع بالعملات الدولية (اليورو، الدولار) والربط مع شركات الشحن العالمية.</li>"
                "<li><strong>شركات التكنولوجيا بفاس شور:</strong> بناء خوادم خلفية متينة وتطبيقات سريعة بتقنيات بايثون ودجانغو.</li>"
                "<li><strong>المصحات والمراكز الطبية:</strong> منصات حجز المواعيد والاطلاع على الفحوصات الطبية بأعلى درجات الأمان وحماية المعطيات الشخصية.</li>"
                "<li><strong>المعاهد والمؤسسات التعليمية:</strong> بوابات تسجيل الطلاب وإدارة المحتوى الأكاديمي والتدريبي.</li>"
                "</ul>"
            ),
            'why_choose_us_en': (
                "<ul>"
                "<li><strong>Dedicated Remote Sprint Team:</strong> Structured weekly milestone delivery with clear video reviews and transparent tracking.</li>"
                "<li><strong>Export & Global E-Commerce Focus:</strong> Proven experience building multi-currency, cross-border storefronts for Moroccan exporters.</li>"
                "<li><strong>Full Multilingual Parity:</strong> Authentic Arabic RTL, French, and English for international and domestic markets.</li>"
                "<li><strong>High-Speed Rail Accessibility:</strong> Easy in-person workshops and strategy sessions whenever required.</li>"
                "</ul>"
            ),
            'why_choose_us_fr': (
                "<ul>"
                "<li><strong>Équipe agile dédiée :</strong> Livraisons hebdomadaires structurées avec démonstrations régulières et suivi transparent.</li>"
                "<li><strong>Expertise en e-commerce d'export :</strong> Expérience éprouvée dans les plateformes multidevises pour exportateurs marocains.</li>"
                "<li><strong>Trilinguisme intégral :</strong> Arabe RTL, français et anglais parfaitement adaptés à vos marchés cibles.</li>"
                "<li><strong>Accessibilité ferroviaire rapide :</strong> Déplacements sur site à Fès facilités pour les phases clés du projet.</li>"
                "</ul>"
            ),
            'why_choose_us_ar': (
                "<ul>"
                "<li><strong>فريق عمل متكامل عن بعد:</strong> تسليم أسبوعي منظم وعروض دورية واضحة لمراحل الإنجاز.</li>"
                "<li><strong>تخصص في التجارة الدولية والتصدير:</strong> خبرة في بناء متاجر تدعم الدفع الدولي وتكامل الشحن السريع.</li>"
                "<li><strong>لغات ثلاث بتنسيق أصيل:</strong> العربية والفرنسية والإنجليزية لتوسيع دائرة الزبائن محلياً ودولياً.</li>"
                "<li><strong>سهولة اللقاءات الحضورية:</strong> إمكانية تنظيم ورشات عمل في فاس عند انطلاق المشاريع.</li>"
                "</ul>"
            ),
            'industries_en': 'Artisanal Export & Manufacturing, Offshoring (Fès Shore), Higher Education, Healthcare & Clinics, Cultural Tourism',
            'industries_fr': 'Artisanat d\'Export & Industrie, Offshoring (Fès Shore), Enseignement Supérieur, Santé & Cliniques, Tourisme Culturel',
            'industries_ar': 'الصناعات التقليدية والتصدير، التعهيد (فاس شور)، التعليم العالي، القطاع الصحي، السياحة الثقافية',
        },
        'web-development-meknes': {
            'h1_en': 'Web Development in Meknès, Morocco',
            'h1_fr': 'Développement Web à Meknès, Maroc',
            'h1_ar': 'تطوير مواقع وتطبيقات الويب في مكناس، المغرب',
            'intro_en': (
                "Delivering custom web platforms, agri-food inventory software, and commercial portals for businesses across Meknès and the Saïss agricultural basin. "
                "Engineered with enterprise precision by our Tangier software studio."
            ),
            'intro_fr': (
                "Création de plateformes web sur mesure, logiciels de gestion de stocks agroalimentaires et portails d'entreprise pour les sociétés de Meknès et du bassin du Saïss. "
                "Conçus avec la rigueur d'ingénierie de notre studio à Tanger."
            ),
            'intro_ar': (
                "نطور منصات ويب مخصصة وبرمجيات لإدارة المخزون والعمليات الزراعية والصناعية لشركات مكناس وسهل سايس. "
                "نهندس برمجياتنا بدقة واحترافية من استوديونا في طنجة."
            ),
            'body_en': (
                "<h3>Digital Systems Driving Modern Enterprise in Meknès</h3>"
                "<p>Meknès is the agro-industrial and manufacturing center of central-northern Morocco. Anchored by the Agropolis cluster—Morocco's foremost competitive agrotech and food-processing zone—along with a major automotive wiring and component assembly presence and extensive commercial distribution networks, the city's economic ecosystem is undergoing rapid technological transformation.</p>"
                "<p>For agricultural producers, olive oil and wine exporters, food processors, and supply chain wholesalers in Meknès, traditional spreadsheets and outdated desktop software create dangerous bottlenecks. getNexiro designs and builds robust, cloud-connected web applications that streamline operations, automate order fulfillment, and connect regional producers directly with buyers across Morocco, Europe, and the Middle East.</p>"
                "<h3>Key Solutions for the Meknès Commercial Corridor</h3>"
                "<p>Our development studio delivers focused, high-return digital systems for Meknès companies:</p>"
                "<ul>"
                "<li><strong>Agri-Food & Export Management Systems:</strong> Custom cloud portals for batch tracking, quality certificate management, international compliance documentation, and export logistics tracking.</li>"
                "<li><strong>B2B Wholesale Ordering Portals:</strong> Secure customer portals allowing retailers and distributors to view dynamic price tiers, check live warehouse inventory, and place recurring orders online.</li>"
                "<li><strong>Automotive & Manufacturing Supplier Dashboards:</strong> Internal production telemetry dashboards and quality control reporting portals for subcontractors operating in Meknès industrial zones.</li>"
                "<li><strong>Corporate & Commercial Web Platforms:</strong> Fast, SEO-optimized multilingual websites that establish market authority and drive qualified enterprise inquiries.</li>"
                "</ul>"
                "<h3>The Tangier-Meknès Strategic Technology Bridge</h3>"
                "<p>Partnering with getNexiro provides Meknès businesses with a dedicated technology team that understands the northern industrial landscape. Operating from Tangier with direct regional transport links, we manage projects through structured sprint releases, clear milestone deliverables, and responsive ongoing maintenance that keeps your mission-critical operations running 24 hours a day, 7 days a week.</p>"
            ),
            'body_fr': (
                "<h3>La Transformation Numérique des Entreprises à Meknès</h3>"
                "<p>Meknès constitue le cœur agro-industriel et manufacturier du centre-nord du Maroc. Autour du pôle de compétitivité Agropolis—première zone intégrée dédiée à l'agro-technologie—et d'un tissu dynamique d'équipementiers automobiles et de distributeurs, la ville connaît une modernisation technologique rapide.</p>"
                "<p>Pour les producteurs agricoles, exportateurs d'huile d'olive, transformateurs et grossistes de Meknès, les tableurs manuels et logiciels obsolètes ralentissent la croissance. getNexiro conçoit des applications web sur mesure hébergées dans le cloud qui automatisent la gestion des commandes, fiabilisent le suivi des stocks et connectent les producteurs aux marchés nationaux et internationaux.</p>"
                "<h3>Solutions Spécifiques pour les Acteurs de Meknès</h3>"
                "<p>Notre équipe déploie des outils digitaux adaptés aux réalités du Saïss :</p>"
                "<ul>"
                "<li><strong>Gestion Agroalimentaire & Export :</strong> Portails de traçabilité des lots, gestion des certificats sanitaires et suivi des expéditions internationales.</li>"
                "<li><strong>Portails de Commandes Grossistes B2B :</strong> Espaces clients sécurisés avec tarification personnalisée, consultation des stocks en temps réel et réassort simplifié.</li>"
                "<li><strong>Tableaux de Bord pour Sous-Traitants Industriels :</strong> Interfaces de suivi de production et contrôle qualité pour les usines du secteur automobile.</li>"
                "<li><strong>Sites Institutionnels et Commerciaux :</strong> Plateformes multilingues rapides et optimisées pour le référencement naturel générant des opportunités d'affaires qualifiées.</li>"
                "</ul>"
            ),
            'body_ar': (
                "<h3>الأنظمة الرقمية لدعم القطاع الفلاحي والصناعي في مكناس</h3>"
                "<p>تمثل مدينة مكناس قطب الصناعات الغذائية والفلاحية الرائد في المغرب، متمركزة حول حظيرة أكروبوليس (Agropolis) المتخصصة، إلى جانب وحدات صناعة كابلات السيارات وتجارة التوزيع الكبرى في حوض سايس، مما يجعل التحول الرقمي خطوة أساسية لتعزيز الإنتاجية.</p>"
                "<p>بالنسبة للمنتجين الزراعيين ومصدري زيت الزيتون والشركات الغذائية وتجار الجملة في مكناس، لم تعد الطرق التقليدية كافية لمواكبة حجم المعاملات. تبتكر جيت نكسيرو (getNexiro) تطبيقات سحابية متطورة تضبط حركة المخزون، وتؤتمت معالجة الطلبيات، وتربط المنتجين المحليين بالأسواق الوطنية والأوروبية مباشرة.</p>"
                "<h3>حلول برمجية مخصصة لشركات مكناس</h3>"
                "<ul>"
                "<li><strong>إدارة الإنتاج الغذائي والتصدير:</strong> بوابات إلكترونية لتتبع دفعات المنتجات وإدارة شهادات الجودة والتصدير للخارج.</li>"
                "<li><strong>بوابات طلبات الجملة بين الشركات (B2B):</strong> منصات لزبائن الجملة تتيح الاطلاع على الأسعار الحصرية والمخزون المتوفر وتقديم الطلبيات فورياً.</li>"
                "<li><strong>لوحات التحكم لمصانع السيارات:</strong> نظم مراقبة جودة الإنتاج وتتبع عمليات التصنيع لموردي أجزاء السيارات.</li>"
                "<li><strong>مواقع مؤسسية متعددة اللغات:</strong> منصات سريعة ومهيأة لمحركات البحث تعزز الثقة وتجلب عقود عمل وشراكات جديدة.</li>"
                "</ul>"
                "<h3>شراكة استراتيجية مستمرة تلائم خصوصية منطقة سايس</h3>"
                "<p>نلتزم في جيت نكسيرو ببناء شراكات طويلة الأمد مع مؤسسات مكناس، عبر تقديم برمجيات آمنة متوافقة مع القوانين المغربية لحماية المعطيات، مع توفير تدريب شامل للفرق التقنية والمستخدمين ودعم فني متواصل يضمن نمو أعمالكم دون توقف.</p>"
            ),
            'why_choose_us_en': (
                "<ul>"
                "<li><strong>Agri-Business & Supply Chain Focus:</strong> Domain expertise in inventory, lot tracking, and export workflows.</li>"
                "<li><strong>Senior Architecture from Tangier:</strong> Cutting-edge Python/Django engineering delivered through structured remote sprints.</li>"
                "<li><strong>Trilingual par excellence:</strong> Flawless Arabic RTL, French, and English interfaces for local staff and international partners.</li>"
                "<li><strong>Reliable Cloud Hosting & Backups:</strong> Mission-critical availability with automated daily encrypted backups.</li>"
                "</ul>"
            ),
            'why_choose_us_fr': (
                "<ul>"
                "<li><strong>Expertise Filière Agro-Industrielle :</strong> Maîtrise des problématiques de traçabilité, stocks et distribution en gros.</li>"
                "<li><strong>Ingénierie avancée depuis Tanger :</strong> Développement moderne sous Python/Django avec livraisons régulières et contrôlées.</li>"
                "<li><strong>Trilinguisme irréprochable :</strong> Interfaces en arabe RTL, français et anglais adaptées aux équipes de terrain et partenaires.</li>"
                "<li><strong>Hébergement cloud sécurisé :</strong> Haute disponibilité et sauvegardes quotidiennes chiffrées automatiques.</li>"
                "</ul>"
            ),
            'why_choose_us_ar': (
                "<ul>"
                "<li><strong>تخصص في سلاسل الإمداد والصناعات الغذائية:</strong> فهم عميق لإدارة المخزون وتتبع المنتجات وعمليات التصدير.</li>"
                "<li><strong>كفاءة هندسية عالية من طنجة:</strong> تطوير برمجي متين بتقنيات دجانغو عبر مراحل تسليم واضحة.</li>"
                "<li><strong>إتقان لغوي متكامل:</strong> واجهات بالعربية والفرنسية والإنجليزية لخدمة الموظفين والشركاء الدوليين.</li>"
                "<li><strong>استضافة سحابية آمنة:</strong> نسخ احتياطي يومي مشفر واستقرار متواصل على مدار الساعة.</li>"
                "</ul>"
            ),
            'industries_en': 'Agribusiness & Food Processing (Agropolis), Automotive Components, Olive Oil & Wine Export, Regional Wholesale Distribution',
            'industries_fr': 'Agroalimentaire & Transformation (Agropolis), Câblage Automobile, Export Huile d\'Olive, Négoce et Gros',
            'industries_ar': 'الصناعات الغذائية والفلاحية (أكروبوليس)، صناعة أجزاء السيارات، تصدير زيت الزيتون، تجارة الجملة والتوزيع',
        },
    }

    for slug, data in city_data.items():
        try:
            page = CityServicePage.objects.get(slug=slug)
        except CityServicePage.DoesNotExist:
            continue

        page.h1_en = data['h1_en']
        page.h1_fr = data['h1_fr']
        page.h1_ar = data['h1_ar']
        page.intro_en = data['intro_en']
        page.intro_fr = data['intro_fr']
        page.intro_ar = data['intro_ar']
        page.body_en = data['body_en']
        page.body_fr = data['body_fr']
        page.body_ar = data['body_ar']
        page.why_choose_us_en = data['why_choose_us_en']
        page.why_choose_us_fr = data['why_choose_us_fr']
        page.why_choose_us_ar = data['why_choose_us_ar']
        page.industries_en = data['industries_en']
        page.industries_fr = data['industries_fr']
        page.industries_ar = data['industries_ar']
        page.save()

def reverse_expand_city_service_content(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_populate_service_deep_content'),
    ]

    operations = [
        migrations.RunPython(expand_city_service_content, reverse_expand_city_service_content),
    ]
