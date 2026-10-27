"""
getNexiro — Core Models with Full Multilingual Support (EN / FR / AR).

All models provide:
  - Multilingual fields (_en, _fr, _ar) for admin editing in every language
  - Smart fallback property access (e.g. obj.title automatically returns
    the current active language version, falling back gracefully to English)
  - Admin dashboard support with language grouping
"""

from django.db import models
from django.utils.translation import gettext_lazy as _, get_language
from django.utils.text import slugify
from django.urls import reverse


def get_localized(instance, field_name):
    """
    Helper to return the localized version of a field based on current request language.
    Priority: current language -> English -> any available non-empty value.
    """
    lang = (get_language() or 'en').lower()
    if lang.startswith('ar'):
        val = getattr(instance, f'{field_name}_ar', None)
        if val:
            return val
    elif lang.startswith('fr'):
        val = getattr(instance, f'{field_name}_fr', None)
        if val:
            return val

    # Default to English
    val_en = getattr(instance, f'{field_name}_en', None)
    if val_en:
        return val_en

    # Fallback to direct field or first non-empty
    for code in ('ar', 'fr'):
        alt = getattr(instance, f'{field_name}_{code}', None)
        if alt:
            return alt
    return ''



# ── 1. Site Configuration (Singleton) ──────────────────────────

class SiteConfig(models.Model):
    """Global site settings with full multilingual text."""

    site_name = models.CharField(
        _('Site Name'), max_length=100, default='getNexiro',
    )

    # Taglines
    tagline_en = models.CharField(_('Tagline (EN)'), max_length=200, default='Tech & Dev Services')
    tagline_fr = models.CharField(_('Tagline (FR)'), max_length=200, blank=True, default='Services Tech & Dev')
    tagline_ar = models.CharField(_('Tagline (AR)'), max_length=200, blank=True, default='خدمات التكنولوجيا والتطوير')

    # Hero Title
    hero_title_en = models.CharField(_('Hero Title (EN)'), max_length=300, default='We Architect High-Velocity Digital Systems')
    hero_title_fr = models.CharField(_('Hero Title (FR)'), max_length=300, blank=True, default='Nous Concevons des Systèmes Numériques Haute-Performance')
    hero_title_ar = models.CharField(_('Hero Title (AR)'), max_length=300, blank=True, default='نصمم أنظمة رقمية عالية السرعة والأداء')

    # Hero Subtitle
    hero_subtitle_en = models.TextField(
        _('Hero Subtitle (EN)'),
        default='A premium software engineering agency crafting scalable web platforms, bespoke enterprise applications, and resilient digital architectures for forward-thinking organizations worldwide.',
    )
    hero_subtitle_fr = models.TextField(
        _('Hero Subtitle (FR)'), blank=True,
        default='Une agence d\'ingénierie logicielle haut de gamme concevant des plateformes web évolutives, des applications d\'entreprise sur mesure et des architectures numériques résilientes pour les organisations visionnaires.',
    )
    hero_subtitle_ar = models.TextField(
        _('Hero Subtitle (AR)'), blank=True,
        default='وكالة رائدة في هندسة البرمجيات تصمم منصات ويب قابلة للتوسع وتطبيقات مؤسسية مخصصة وبنيات تحتية رقمية مرنة للمؤسسات الطموحة في المغرب والعالم.',
    )

    # About Text
    about_text_en = models.TextField(
        _('About Us (EN)'), blank=True,
        default="Founded in Tangier — the vibrant city where the Atlantic meets the Mediterranean — getNexiro was born from a simple belief: world-class software doesn't need a Silicon Valley address.",
    )
    about_text_fr = models.TextField(
        _('About Us (FR)'), blank=True,
        default="Fondée à Tanger — la ville vibrante où l'Atlantique rencontre la Méditerranée — getNexiro est née d'une conviction simple : les logiciels de classe mondiale n'ont pas besoin d'une adresse dans la Silicon Valley.",
    )
    about_text_ar = models.TextField(
        _('About Us (AR)'), blank=True,
        default="تأسست getNexiro في طنجة — المدينة النابضة بالحياة حيث يلتقي الأطلسي بالمتوسط — من إيمان راسخ: البرمجيات العالمية لا تحتاج إلى عنوان في وادي السيليكون.",
    )

    # Mission Statement
    mission_statement_en = models.TextField(
        _('Mission (EN)'), blank=True,
        default='To empower enterprises with bespoke digital solutions that are not just functional, but transformative — combining technical excellence with strategic insight to create lasting competitive advantages.',
    )
    mission_statement_fr = models.TextField(
        _('Mission (FR)'), blank=True,
        default='Donner aux entreprises les moyens d\'agir grâce à des solutions numériques sur mesure qui ne sont pas seulement fonctionnelles, mais transformatrices — alliant excellence technique et vision stratégique.',
    )
    mission_statement_ar = models.TextField(
        _('Mission (AR)'), blank=True,
        default='تمكين الشركات من خلال حلول رقمية مخصصة ليست فقط وظيفية، بل تحويلية — تجمع بين التميز الهندسي والرؤية الاستراتيجية لتحقيق ميزة تنافسية مستدامة.',
    )

    # Contact & location
    email = models.EmailField(_('Contact Email'), default='getnexiro@gmail.com')
    phone = models.CharField(_('Phone Number'), max_length=30, default='+212 663 017 817')

    address_en = models.CharField(_('Address (EN)'), max_length=200, default='Tangier 90000, Morocco')
    address_fr = models.CharField(_('Address (FR)'), max_length=200, blank=True, default='Tanger 90000, Maroc')
    address_ar = models.CharField(_('Address (AR)'), max_length=200, blank=True, default='طنجة 90000، المغرب')

    address_detail_en = models.CharField(_('Address Detail (EN)'), max_length=200, default='Ibn Batouta Bureaux, Av. Youssef Ibn Tachfine')
    address_detail_fr = models.CharField(_('Address Detail (FR)'), max_length=200, blank=True, default='Bureaux Ibn Batouta, Av. Youssef Ibn Tachfine')
    address_detail_ar = models.CharField(_('Address Detail (AR)'), max_length=200, blank=True, default='مكاتب ابن بطوطة، شارع يوسف بن تاشفين')

    business_hours_en = models.CharField(_('Business Hours (EN)'), max_length=100, default='Mon — Fri: 9:00 AM — 6:00 PM (GMT+1)')
    business_hours_fr = models.CharField(_('Business Hours (FR)'), max_length=100, blank=True, default='Lun — Ven : 9h00 — 18h00 (GMT+1)')
    business_hours_ar = models.CharField(_('Business Hours (AR)'), max_length=100, blank=True, default='الإثنين — الجمعة: 9:00 ص — 6:00 م (GMT+1)')

    map_embed_url = models.URLField(
        _('Map Embed URL'), blank=True,
        default='https://www.openstreetmap.org/export/embed.html?bbox=-5.83%2C35.76%2C-5.79%2C35.79&layer=mapnik&marker=35.7796%2C-5.8030',
    )

    # Social links
    instagram_url = models.URLField(_('Instagram URL'), blank=True, default='https://www.instagram.com/getnexiro')
    linkedin_url = models.URLField(_('LinkedIn URL'), blank=True, default='')
    github_url = models.URLField(_('GitHub URL'), blank=True, default='https://github.com/simoderkaoui/getnexiro')
    twitter_url = models.URLField(_('Twitter / X URL'), blank=True, default='')

    # SEO Meta Descriptions
    meta_description_en = models.CharField(_('Meta Description (EN)'), max_length=300, blank=True, default='getNexiro — Professional web development, mobile apps & software engineering agency in Tangier, Morocco.')
    meta_description_fr = models.CharField(_('Meta Description (FR)'), max_length=300, blank=True, default='getNexiro — Agence de développement web, applications mobiles et ingénierie logicielle à Tanger, Maroc.')
    meta_description_ar = models.CharField(_('Meta Description (AR)'), max_length=300, blank=True, default='getNexiro — وكالة رائدة في تطوير المواقع وتطبيقات الجوال وهندسة البرمجيات في طنجة، المغرب.')

    # Branding & Pictures
    site_logo = models.ImageField(_('Site Logo'), upload_to='branding/', blank=True, null=True, help_text=_('Website header logo (transparent PNG recommended)'))
    site_favicon = models.FileField(_('Site Favicon / Icon'), upload_to='branding/', blank=True, null=True)
    about_image = models.ImageField(_('About Page Image'), upload_to='about/', blank=True, null=True, help_text=_('Feature picture for About Us page (Tangier / Studio image)'))

    # Hero Video & Wallpaper Settings
    HERO_BG_CHOICES = [
        ('default', _('Default Animated Mesh / Glow')),
        ('image', _('Custom Wallpaper / Image')),
        ('video', _('Video Background')),
    ]
    hero_bg_type = models.CharField(_('Hero Background Type'), max_length=20, choices=HERO_BG_CHOICES, default='default')
    hero_bg_image = models.ImageField(_('Hero Wallpaper / Background Image'), upload_to='hero/', blank=True, null=True)
    hero_bg_video = models.FileField(_('Hero Background Video (MP4/WebM)'), upload_to='hero/', blank=True, null=True)
    hero_bg_video_url = models.URLField(_('Hero Background Video URL (Direct MP4 or external)'), blank=True, default='')

    # Page Header Background Videos (Per Page)
    about_bg_video = models.FileField(_('About Page Video (MP4/WebM)'), upload_to='headers/', blank=True, null=True, help_text=_('Custom video background for About page header'))
    about_bg_video_url = models.URLField(_('About Page Video URL'), blank=True, default='', help_text=_('Direct MP4/WebM URL for About page header'))

    services_bg_video = models.FileField(_('Services Page Video (MP4/WebM)'), upload_to='headers/', blank=True, null=True, help_text=_('Custom video background for Services page header'))
    services_bg_video_url = models.URLField(_('Services Page Video URL'), blank=True, default='', help_text=_('Direct MP4/WebM URL for Services page header'))

    projects_bg_video = models.FileField(_('Projects Page Video (MP4/WebM)'), upload_to='headers/', blank=True, null=True, help_text=_('Custom video background for Projects page header'))
    projects_bg_video_url = models.URLField(_('Projects Page Video URL'), blank=True, default='', help_text=_('Direct MP4/WebM URL for Projects page header'))

    blog_bg_video = models.FileField(_('Blog Page Video (MP4/WebM)'), upload_to='headers/', blank=True, null=True, help_text=_('Custom video background for Blog page header'))
    blog_bg_video_url = models.URLField(_('Blog Page Video URL'), blank=True, default='', help_text=_('Direct MP4/WebM URL for Blog page header'))

    contact_bg_video = models.FileField(_('Contact Page Video (MP4/WebM)'), upload_to='headers/', blank=True, null=True, help_text=_('Custom video background for Contact page header'))
    contact_bg_video_url = models.URLField(_('Contact Page Video URL'), blank=True, default='', help_text=_('Direct MP4/WebM URL for Contact page header'))


    # Hero Badges & Buttons
    hero_badge_en = models.CharField(_('Hero Badge (EN)'), max_length=150, default='B2B Software Studio • Tangier, Morocco')
    hero_badge_fr = models.CharField(_('Hero Badge (FR)'), max_length=150, blank=True, default='Studio Logiciel B2B • Tanger, Maroc')
    hero_badge_ar = models.CharField(_('Hero Badge (AR)'), max_length=150, blank=True, default='استوديو برمجيات B2B • طنجة، المغرب')

    hero_cta_primary_text_en = models.CharField(_('Hero CTA Primary (EN)'), max_length=60, default='Start a Project')
    hero_cta_primary_text_fr = models.CharField(_('Hero CTA Primary (FR)'), max_length=60, blank=True, default='Démarrer un projet')
    hero_cta_primary_text_ar = models.CharField(_('Hero CTA Primary (AR)'), max_length=60, blank=True, default='ابدأ مشروعك')

    hero_cta_secondary_text_en = models.CharField(_('Hero CTA Secondary (EN)'), max_length=60, default='Selected Work')
    hero_cta_secondary_text_fr = models.CharField(_('Hero CTA Secondary (FR)'), max_length=60, blank=True, default='Nos Réalisations')
    hero_cta_secondary_text_ar = models.CharField(_('Hero CTA Secondary (AR)'), max_length=60, blank=True, default='أعمال مختارة')

    # Global CTA Banner
    cta_title_en = models.CharField(_('CTA Title (EN)'), max_length=200, default='Ready to Architect Your Next Digital Leap?')
    cta_title_fr = models.CharField(_('CTA Title (FR)'), max_length=200, blank=True, default='Prêt à concevoir votre prochain saut numérique ?')
    cta_title_ar = models.CharField(_('CTA Title (AR)'), max_length=200, blank=True, default='هل أنت مستعد لبناء مشروعك الرقمي القادم؟')

    cta_subtitle_en = models.TextField(_('CTA Subtitle (EN)'), default='Schedule an architecture consultation with our engineering team in Tangier.')
    cta_subtitle_fr = models.TextField(_('CTA Subtitle (FR)'), blank=True, default='Planifiez une consultation d\'architecture avec notre équipe d\'ingénierie à Tanger.')
    cta_subtitle_ar = models.TextField(_('CTA Subtitle (AR)'), blank=True, default='احجز جلسة استشارية تقنية مع فريقنا الهندسي في طنجة.')

    cta_button_text_en = models.CharField(_('CTA Button (EN)'), max_length=60, default='Start Your Project')
    cta_button_text_fr = models.CharField(_('CTA Button (FR)'), max_length=60, blank=True, default='Démarrer votre projet')
    cta_button_text_ar = models.CharField(_('CTA Button (AR)'), max_length=60, blank=True, default='ابدأ مشروعك معنا')

    # Localized Property Getters
    @property
    def tagline(self): return get_localized(self, 'tagline')

    @property
    def hero_badge(self): return get_localized(self, 'hero_badge')

    @property
    def hero_title(self): return get_localized(self, 'hero_title')

    @property
    def hero_subtitle(self): return get_localized(self, 'hero_subtitle')

    @property
    def hero_cta_primary_text(self): return get_localized(self, 'hero_cta_primary_text')

    @property
    def hero_cta_secondary_text(self): return get_localized(self, 'hero_cta_secondary_text')

    @property
    def cta_title(self): return get_localized(self, 'cta_title')

    @property
    def cta_subtitle(self): return get_localized(self, 'cta_subtitle')

    @property
    def cta_button_text(self): return get_localized(self, 'cta_button_text')

    @property
    def about_text(self): return get_localized(self, 'about_text')

    @property
    def mission_statement(self): return get_localized(self, 'mission_statement')

    @property
    def address(self): return get_localized(self, 'address')

    @property
    def address_detail(self): return get_localized(self, 'address_detail')

    @property
    def business_hours(self): return get_localized(self, 'business_hours')

    @property
    def meta_description(self): return get_localized(self, 'meta_description')

    class Meta:
        verbose_name = _('Site Configuration')
        verbose_name_plural = _('Site Configuration')

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ── 2. Services ────────────────────────────────────────────────

class Service(models.Model):
    """Service offerings with full multilingual title and description."""

    ICON_CHOICES = [
        ('icon-web', _('Web / Globe')),
        ('icon-mobile', _('Mobile / Phone')),
        ('icon-design', _('Design / Pen')),
        ('icon-consulting', _('Consulting / Briefcase')),
        ('icon-api', _('API / Code')),
        ('icon-cloud', _('Cloud / DevOps')),
        ('icon-security', _('Security / Shield')),
        ('icon-data', _('Data / Database')),
    ]

    title_en = models.CharField(_('Title (EN)'), max_length=120)
    title_fr = models.CharField(_('Title (FR)'), max_length=120, blank=True, default='')
    title_ar = models.CharField(_('Title (AR)'), max_length=120, blank=True, default='')

    slug = models.SlugField(_('Slug'), max_length=150, unique=True, null=True, blank=True)

    subtitle_en = models.CharField(_('Tagline / Subtitle (EN)'), max_length=250, blank=True, default='')
    subtitle_fr = models.CharField(_('Tagline / Subtitle (FR)'), max_length=250, blank=True, default='')
    subtitle_ar = models.CharField(_('Tagline / Subtitle (AR)'), max_length=250, blank=True, default='')

    description_en = models.TextField(_('Overview (EN)'))
    description_fr = models.TextField(_('Overview (FR)'), blank=True, default='')
    description_ar = models.TextField(_('Overview (AR)'), blank=True, default='')

    # Deep Details: Methodology, Deliverables & Specifications
    methodology_en = models.TextField(_('Engineering Methodology (EN)'), blank=True, default='')
    methodology_fr = models.TextField(_('Engineering Methodology (FR)'), blank=True, default='')
    methodology_ar = models.TextField(_('Engineering Methodology (AR)'), blank=True, default='')

    deliverables_en = models.TextField(_('Core Deliverables (EN, newline-separated)'), blank=True, default='')
    deliverables_fr = models.TextField(_('Core Deliverables (FR, newline-separated)'), blank=True, default='')
    deliverables_ar = models.TextField(_('Core Deliverables (AR, newline-separated)'), blank=True, default='')

    technologies = models.CharField(_('Technologies & Stacks (comma-separated)'), max_length=300, blank=True)
    timeline = models.CharField(_('Typical Timeline'), max_length=60, blank=True, default='4 — 8 Weeks')

    icon = models.CharField(
        _('Icon'), max_length=30, choices=ICON_CHOICES, default='icon-web',
    )
    is_featured = models.BooleanField(
        _('Featured on Home Page'), default=False,
    )
    order = models.PositiveIntegerField(_('Display Order'), default=0)

    @property
    def title(self): return get_localized(self, 'title')

    @property
    def subtitle(self): return get_localized(self, 'subtitle')

    @property
    def description(self): return get_localized(self, 'description')

    @property
    def methodology(self): return get_localized(self, 'methodology')

    @property
    def deliverables(self): return get_localized(self, 'deliverables')

    @property
    def deliverables_list(self):
        text = self.deliverables
        if not text:
            return []
        return [line.strip().lstrip('-•* ') for line in text.splitlines() if line.strip()]

    @property
    def tech_list(self):
        if not self.technologies:
            return []
        return [t.strip() for t in self.technologies.split(',') if t.strip()]

    def get_absolute_url(self):
        return reverse('core:service_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title_en or f'service-{self.pk or ""}')
            if not base_slug:
                base_slug = 'service'
            slug = base_slug
            counter = 1
            while Service.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['order', 'pk']

    def __str__(self):
        return self.title_en or self.title_ar or f"Service #{self.pk}"


class ServiceSolution(models.Model):
    """Specific solution module/capability under a service."""

    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='solutions',
        verbose_name=_('Service'),
    )
    title_en = models.CharField(_('Solution Title (EN)'), max_length=150)
    title_fr = models.CharField(_('Solution Title (FR)'), max_length=150, blank=True, default='')
    title_ar = models.CharField(_('Solution Title (AR)'), max_length=150, blank=True, default='')

    description_en = models.TextField(_('Solution Description (EN)'))
    description_fr = models.TextField(_('Solution Description (FR)'), blank=True, default='')
    description_ar = models.TextField(_('Solution Description (AR)'), blank=True, default='')

    icon_emoji = models.CharField(_('Emoji Icon'), max_length=10, default='⚡')
    order = models.PositiveIntegerField(_('Display Order'), default=0)

    @property
    def title(self): return get_localized(self, 'title')

    @property
    def description(self): return get_localized(self, 'description')

    class Meta:
        verbose_name = _('Service Solution')
        verbose_name_plural = _('Service Solutions')
        ordering = ['order', 'pk']

    def __str__(self):
        return f"{self.service.title_en} — {self.title_en}"



# ── 3. Project Categories ──────────────────────────────────────

class ProjectCategory(models.Model):
    """Categories for portfolio projects."""

    name_en = models.CharField(_('Name (EN)'), max_length=80)
    name_fr = models.CharField(_('Name (FR)'), max_length=80, blank=True, default='')
    name_ar = models.CharField(_('Name (AR)'), max_length=80, blank=True, default='')
    slug = models.SlugField(_('Slug'), unique=True)

    @property
    def name(self): return get_localized(self, 'name')

    class Meta:
        verbose_name = _('Project Category')
        verbose_name_plural = _('Project Categories')
        ordering = ['name_en']

    def __str__(self):
        return self.name_en or self.name_ar or self.slug


# ── 4. Projects ────────────────────────────────────────────────

class Project(models.Model):
    """Portfolio case studies."""

    title_en = models.CharField(_('Title (EN)'), max_length=150)
    title_fr = models.CharField(_('Title (FR)'), max_length=150, blank=True, default='')
    title_ar = models.CharField(_('Title (AR)'), max_length=150, blank=True, default='')

    slug = models.SlugField(_('Slug'), max_length=160, unique=True, null=True, blank=True)

    category = models.ForeignKey(
        ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name=_('Category'),
    )

    # Executive Summary / Overview
    description_en = models.TextField(_('Overview (EN)'))
    description_fr = models.TextField(_('Overview (FR)'), blank=True, default='')
    description_ar = models.TextField(_('Overview (AR)'), blank=True, default='')

    image = models.ImageField(
        _('Cover Image'), upload_to='projects/', blank=True, null=True,
    )
    client_name = models.CharField(_('Client Name'), max_length=100, blank=True)
    technologies = models.CharField(_('Technologies (comma-separated)'), max_length=300, blank=True)
    duration = models.CharField(_('Duration'), max_length=60, blank=True, default='3 Months')
    year = models.CharField(_('Year'), max_length=20, blank=True, default='2025')
    live_url = models.URLField(_('Live Project URL'), blank=True, help_text=_('Link to live website or production application'))
    github_url = models.URLField(_('GitHub / Source URL'), blank=True)

    # Deep-Dive Case Study Sections (Multilingual)
    challenge_en = models.TextField(_('The Challenge (EN)'), blank=True, default='')
    challenge_fr = models.TextField(_('The Challenge (FR)'), blank=True, default='')
    challenge_ar = models.TextField(_('The Challenge (AR)'), blank=True, default='')

    solution_en = models.TextField(_('Architecture & Solution (EN)'), blank=True, default='')
    solution_fr = models.TextField(_('Architecture & Solution (FR)'), blank=True, default='')
    solution_ar = models.TextField(_('Architecture & Solution (AR)'), blank=True, default='')

    results_en = models.TextField(_('Results & Impact (EN)'), blank=True, default='')
    results_fr = models.TextField(_('Results & Impact (FR)'), blank=True, default='')
    results_ar = models.TextField(_('Results & Impact (AR)'), blank=True, default='')

    # Client Feedback / Quote
    client_feedback_quote_en = models.TextField(_('Client Testimonial Quote (EN)'), blank=True, default='')
    client_feedback_quote_fr = models.TextField(_('Client Testimonial Quote (FR)'), blank=True, default='')
    client_feedback_quote_ar = models.TextField(_('Client Testimonial Quote (AR)'), blank=True, default='')
    client_feedback_author = models.CharField(_('Client Testimonial Author'), max_length=100, blank=True, default='')
    client_feedback_role = models.CharField(_('Client Testimonial Role'), max_length=120, blank=True, default='')

    is_featured = models.BooleanField(_('Featured on Home Page'), default=False)
    order = models.PositiveIntegerField(_('Display Order'), default=0)
    created_at = models.DateField(_('Project Date'), auto_now_add=True)

    @property
    def title(self): return get_localized(self, 'title')

    @property
    def description(self): return get_localized(self, 'description')

    @property
    def challenge(self): return get_localized(self, 'challenge')

    @property
    def solution(self): return get_localized(self, 'solution')

    @property
    def results(self): return get_localized(self, 'results')

    @property
    def client_feedback_quote(self): return get_localized(self, 'client_feedback_quote')

    @property
    def tech_list(self):
        """Returns clean list of technologies."""
        if not self.technologies:
            return []
        return [t.strip() for t in self.technologies.split(',') if t.strip()]

    def get_absolute_url(self):
        return reverse('core:project_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title_en or f'project-{self.pk or ""}')
            if not base_slug:
                base_slug = 'project'
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title_en or self.title_ar or f"Project #{self.pk}"


class ProjectImage(models.Model):
    """Gallery carousel images for a project case study."""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='gallery_images',
        verbose_name=_('Project'),
    )
    image = models.ImageField(_('Gallery Image'), upload_to='projects/gallery/')
    caption_en = models.CharField(_('Caption (EN)'), max_length=200, blank=True, default='')
    caption_fr = models.CharField(_('Caption (FR)'), max_length=200, blank=True, default='')
    caption_ar = models.CharField(_('Caption (AR)'), max_length=200, blank=True, default='')
    order = models.PositiveIntegerField(_('Display Order'), default=0)

    @property
    def caption(self): return get_localized(self, 'caption')

    class Meta:
        verbose_name = _('Project Gallery Image')
        verbose_name_plural = _('Project Gallery Images')
        ordering = ['order', 'pk']

    def __str__(self):
        return f"{self.project.title_en} — Image #{self.pk}"



# ── 5. Team Members ────────────────────────────────────────────

class TeamMember(models.Model):
    """Team members on About page."""

    name = models.CharField(_('Full Name'), max_length=100)

    role_en = models.CharField(_('Role (EN)'), max_length=120)
    role_fr = models.CharField(_('Role (FR)'), max_length=120, blank=True, default='')
    role_ar = models.CharField(_('Role (AR)'), max_length=120, blank=True, default='')

    bio_en = models.TextField(_('Bio (EN)'), blank=True, default='')
    bio_fr = models.TextField(_('Bio (FR)'), blank=True, default='')
    bio_ar = models.TextField(_('Bio (AR)'), blank=True, default='')

    photo = models.ImageField(_('Photo'), upload_to='team/', blank=True, null=True)
    linkedin_url = models.URLField(_('LinkedIn URL'), blank=True)
    order = models.PositiveIntegerField(_('Display Order'), default=0)

    @property
    def role(self): return get_localized(self, 'role')

    @property
    def bio(self): return get_localized(self, 'bio')

    class Meta:
        verbose_name = _('Team Member')
        verbose_name_plural = _('Team Members')
        ordering = ['order', 'pk']

    def __str__(self):
        return self.name


# ── 6. Testimonials ────────────────────────────────────────────

class Testimonial(models.Model):
    """Client testimonials."""

    quote_en = models.TextField(_('Quote (EN)'))
    quote_fr = models.TextField(_('Quote (FR)'), blank=True, default='')
    quote_ar = models.TextField(_('Quote (AR)'), blank=True, default='')

    author_name = models.CharField(_('Author Name'), max_length=100)

    author_role_en = models.CharField(_('Author Role (EN)'), max_length=100, blank=True, default='')
    author_role_fr = models.CharField(_('Author Role (FR)'), max_length=100, blank=True, default='')
    author_role_ar = models.CharField(_('Author Role (AR)'), max_length=100, blank=True, default='')

    company = models.CharField(_('Company'), max_length=100, blank=True)
    avatar = models.ImageField(_('Avatar'), upload_to='testimonials/', blank=True)
    is_featured = models.BooleanField(_('Show on Home'), default=True)
    order = models.PositiveIntegerField(_('Display Order'), default=0)

    @property
    def quote(self): return get_localized(self, 'quote')

    @property
    def author_role(self): return get_localized(self, 'author_role')

    class Meta:
        verbose_name = _('Testimonial')
        verbose_name_plural = _('Testimonials')
        ordering = ['order', 'pk']

    def __str__(self):
        return f'{self.author_name} — {self.company}'


# ── 7. Client Logos ────────────────────────────────────────────

class ClientLogo(models.Model):
    name = models.CharField(_('Company Name'), max_length=100)
    logo = models.ImageField(_('Logo Image'), upload_to='clients/')
    url = models.URLField(_('Company URL'), blank=True)
    order = models.PositiveIntegerField(_('Display Order'), default=0)

    class Meta:
        verbose_name = _('Client Logo')
        verbose_name_plural = _('Client Logos')
        ordering = ['order']

    def __str__(self):
        return self.name


# ── 8. Statistics ──────────────────────────────────────────────

class Stat(models.Model):
    """Impact statistics with multilingual labels."""

    value = models.CharField(_('Value'), max_length=30)

    label_en = models.CharField(_('Label (EN)'), max_length=120)
    label_fr = models.CharField(_('Label (FR)'), max_length=120, blank=True, default='')
    label_ar = models.CharField(_('Label (AR)'), max_length=120, blank=True, default='')

    order = models.PositiveIntegerField(_('Display Order'), default=0)

    @property
    def label(self): return get_localized(self, 'label')

    class Meta:
        verbose_name = _('Statistic')
        verbose_name_plural = _('Statistics')
        ordering = ['order']

    def __str__(self):
        return f'{self.value} — {self.label_en}'


# ── 9. Contact Message ─────────────────────────────────────────

class ContactMessage(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'))
    subject = models.CharField(_('Subject'), max_length=200)
    message = models.TextField(_('Message'))
    created_at = models.DateTimeField(_('Received At'), auto_now_add=True)
    is_read = models.BooleanField(_('Read'), default=False)

    class Meta:
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.subject}'


# ── 10. Company Values (About Page) ────────────────────────────

class CompanyValue(models.Model):
    """Company core values displayed on the About page."""

    icon = models.CharField(_('Icon / Emoji'), max_length=30, default='🌍', help_text=_('Emoji or symbol, e.g. 🌍, 💡, 💎'))
    title_en = models.CharField(_('Title (EN)'), max_length=120)
    title_fr = models.CharField(_('Title (FR)'), max_length=120, blank=True, default='')
    title_ar = models.CharField(_('Title (AR)'), max_length=120, blank=True, default='')

    description_en = models.TextField(_('Description (EN)'))
    description_fr = models.TextField(_('Description (FR)'), blank=True, default='')
    description_ar = models.TextField(_('Description (AR)'), blank=True, default='')

    order = models.PositiveIntegerField(_('Display Order'), default=0)

    @property
    def title(self): return get_localized(self, 'title')

    @property
    def description(self): return get_localized(self, 'description')

    class Meta:
        verbose_name = _('Company Value')
        verbose_name_plural = _('Company Values')
        ordering = ['order', 'pk']

    def __str__(self):
        return self.title_en or f"Value #{self.pk}"


# ── 11. Process Steps (Services Page) ──────────────────────────

class ProcessStep(models.Model):
    """4-step delivery process displayed on the Services page."""

    step_number = models.CharField(_('Step Number'), max_length=10, default='01', help_text=_('e.g. 01, 02, 03, 04'))
    title_en = models.CharField(_('Title (EN)'), max_length=120)
    title_fr = models.CharField(_('Title (FR)'), max_length=120, blank=True, default='')
    title_ar = models.CharField(_('Title (AR)'), max_length=120, blank=True, default='')

    description_en = models.TextField(_('Description (EN)'))
    description_fr = models.TextField(_('Description (FR)'), blank=True, default='')
    description_ar = models.TextField(_('Description (AR)'), blank=True, default='')

    tags = models.CharField(_('Tags (comma-separated)'), max_length=200, blank=True, default='Discovery, Planning')
    order = models.PositiveIntegerField(_('Display Order'), default=0)

    @property
    def title(self): return get_localized(self, 'title')

    @property
    def description(self): return get_localized(self, 'description')

    class Meta:
        verbose_name = _('Process Step')
        verbose_name_plural = _('Process Steps')
        ordering = ['order', 'pk']

    def __str__(self):
        return f"{self.step_number} — {self.title_en}"


# ── 12. Blog ───────────────────────────────────────────────────

class BlogCategory(models.Model):
    """Blog post categories."""

    name_en = models.CharField(_('Name (EN)'), max_length=80)
    name_fr = models.CharField(_('Name (FR)'), max_length=80, blank=True, default='')
    name_ar = models.CharField(_('Name (AR)'), max_length=80, blank=True, default='')
    slug = models.SlugField(_('Slug'), unique=True)

    @property
    def name(self): return get_localized(self, 'name')

    class Meta:
        verbose_name = _('Blog Category')
        verbose_name_plural = _('Blog Categories')
        ordering = ['name_en']

    def __str__(self):
        return self.name_en or self.slug


class BlogPost(models.Model):
    """SEO-optimized blog posts with full multilingual support."""

    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('published', _('Published')),
    ]

    # Core content
    title_en = models.CharField(_('Title (EN)'), max_length=250)
    title_fr = models.CharField(_('Title (FR)'), max_length=250, blank=True, default='')
    title_ar = models.CharField(_('Title (AR)'), max_length=250, blank=True, default='')

    slug = models.SlugField(_('URL Slug'), max_length=280, unique=True, null=True, blank=True)

    excerpt_en = models.TextField(_('Excerpt / Summary (EN)'), max_length=500, blank=True, default='')
    excerpt_fr = models.TextField(_('Excerpt / Summary (FR)'), max_length=500, blank=True, default='')
    excerpt_ar = models.TextField(_('Excerpt / Summary (AR)'), max_length=500, blank=True, default='')

    body_en = models.TextField(_('Body (EN)'))
    body_fr = models.TextField(_('Body (FR)'), blank=True, default='')
    body_ar = models.TextField(_('Body (AR)'), blank=True, default='')

    # SEO meta
    meta_title_en = models.CharField(_('SEO Title (EN)'), max_length=70, blank=True, default='', help_text=_('Overrides title in <title> tag. Max 70 chars.'))
    meta_title_fr = models.CharField(_('SEO Title (FR)'), max_length=70, blank=True, default='')
    meta_title_ar = models.CharField(_('SEO Title (AR)'), max_length=70, blank=True, default='')

    meta_description_en = models.CharField(_('Meta Description (EN)'), max_length=160, blank=True, default='', help_text=_('Google snippet. Max 160 chars.'))
    meta_description_fr = models.CharField(_('Meta Description (FR)'), max_length=160, blank=True, default='')
    meta_description_ar = models.CharField(_('Meta Description (AR)'), max_length=160, blank=True, default='')

    meta_keywords = models.CharField(_('Meta Keywords (comma-separated)'), max_length=300, blank=True, default='')

    # Taxonomy & media
    category = models.ForeignKey(
        BlogCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='posts', verbose_name=_('Category'),
    )
    featured_image = models.ImageField(_('Featured Image'), upload_to='blog/', blank=True, null=True)
    featured_image_alt = models.CharField(_('Image Alt Text'), max_length=200, blank=True, default='')

    # Author & metadata
    author_name = models.CharField(_('Author Name'), max_length=100, default='getNexiro Team')
    reading_time_minutes = models.PositiveIntegerField(_('Reading Time (minutes)'), default=5)
    tags = models.CharField(_('Tags (comma-separated)'), max_length=300, blank=True, default='')

    # Publishing
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(_('Featured'), default=False)
    published_at = models.DateTimeField(_('Published At'), null=True, blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    @property
    def title(self): return get_localized(self, 'title')

    @property
    def excerpt(self): return get_localized(self, 'excerpt')

    @property
    def body(self): return get_localized(self, 'body')

    @property
    def meta_title(self):
        val = get_localized(self, 'meta_title')
        return val if val else self.title

    @property
    def meta_description(self):
        val = get_localized(self, 'meta_description')
        return val if val else self.excerpt[:160]

    @property
    def tags_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    def get_absolute_url(self):
        return reverse('core:blog_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title_en or f'post-{self.pk or ""}')
            if not base_slug:
                base_slug = 'post'
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Blog Post')
        verbose_name_plural = _('Blog Posts')
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title_en or f"Post #{self.pk}"


# ── 13. Store Items (Hidden — Coming Later) ────────────────────

class StoreItem(models.Model):
    """Upcoming products/templates displayed on the Store page."""

    emoji = models.CharField(_('Emoji / Icon'), max_length=20, default='🚀')
    title_en = models.CharField(_('Title (EN)'), max_length=120)
    title_fr = models.CharField(_('Title (FR)'), max_length=120, blank=True, default='')
    title_ar = models.CharField(_('Title (AR)'), max_length=120, blank=True, default='')

    description_en = models.TextField(_('Description (EN)'))
    description_fr = models.TextField(_('Description (FR)'), blank=True, default='')
    description_ar = models.TextField(_('Description (AR)'), blank=True, default='')

    badge_en = models.CharField(_('Badge (EN)'), max_length=50, blank=True, default='COMING SOON')
    badge_fr = models.CharField(_('Badge (FR)'), max_length=50, blank=True, default='BIENTÔT DISPONIBLE')
    badge_ar = models.CharField(_('Badge (AR)'), max_length=50, blank=True, default='قريباً')

    order = models.PositiveIntegerField(_('Display Order'), default=0)
    is_active = models.BooleanField(_('Active'), default=True)

    @property
    def title(self): return get_localized(self, 'title')

    @property
    def description(self): return get_localized(self, 'description')

    @property
    def badge(self): return get_localized(self, 'badge')

    class Meta:
        verbose_name = _('Store Item')
        verbose_name_plural = _('Store Items')
        ordering = ['order', 'pk']

    def __str__(self):
        return self.title_en or f"Store Item #{self.pk}"



# ── 14. Legal Pages (Privacy Policy, Terms, etc.) ──────────────

class LegalPage(models.Model):
    """Admin-editable legal/policy pages (Privacy Policy, Terms of Service, etc.)."""

    SLUG_CHOICES = [
        ('privacy-policy', _('Privacy Policy')),
        ('terms-of-service', _('Terms of Service')),
    ]

    slug = models.SlugField(_('Page Identifier'), max_length=80, unique=True, choices=SLUG_CHOICES)

    title_en = models.CharField(_('Title (EN)'), max_length=200)
    title_fr = models.CharField(_('Title (FR)'), max_length=200, blank=True, default='')
    title_ar = models.CharField(_('Title (AR)'), max_length=200, blank=True, default='')

    body_en = models.TextField(_('Content (EN)'), help_text=_('HTML allowed. Use headings, paragraphs, lists.'))
    body_fr = models.TextField(_('Content (FR)'), blank=True, default='')
    body_ar = models.TextField(_('Content (AR)'), blank=True, default='')

    updated_at = models.DateTimeField(_('Last Updated'), auto_now=True)

    @property
    def title(self): return get_localized(self, 'title')

    @property
    def body(self): return get_localized(self, 'body')

    class Meta:
        verbose_name = _('Legal Page')
        verbose_name_plural = _('Legal Pages')
        ordering = ['slug']

    def __str__(self):
        return self.title_en or self.slug


# ── 15. FAQ ────────────────────────────────────────────────────

class FAQ(models.Model):
    """Frequently Asked Questions displayed on home, services, and packages pages."""

    SECTION_CHOICES = [
        ('general', _('General')),
        ('services', _('Services')),
        ('pricing', _('Pricing & Packages')),
        ('process', _('Process & Delivery')),
    ]

    question_en = models.CharField(_('Question (EN)'), max_length=300)
    question_fr = models.CharField(_('Question (FR)'), max_length=300, blank=True, default='')
    question_ar = models.CharField(_('Question (AR)'), max_length=300, blank=True, default='')

    answer_en = models.TextField(_('Answer (EN)'))
    answer_fr = models.TextField(_('Answer (FR)'), blank=True, default='')
    answer_ar = models.TextField(_('Answer (AR)'), blank=True, default='')

    section = models.CharField(_('Section'), max_length=30, choices=SECTION_CHOICES, default='general')
    order = models.PositiveIntegerField(_('Display Order'), default=0)
    is_active = models.BooleanField(_('Active'), default=True)

    @property
    def question(self): return get_localized(self, 'question')

    @property
    def answer(self): return get_localized(self, 'answer')

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
        ordering = ['section', 'order', 'pk']

    def __str__(self):
        return self.question_en[:80] or f"FAQ #{self.pk}"


# ══════════════════════════════════════════════════════════════════
# PHASE 2: Lead Generation Models
# ══════════════════════════════════════════════════════════════════


# ── 16. Pricing Packages ───────────────────────────────────────

class Package(models.Model):
    """Admin-editable pricing packages (Showcase, E-commerce, Custom Platform, etc.)."""

    name_en = models.CharField(_('Package Name (EN)'), max_length=120)
    name_fr = models.CharField(_('Package Name (FR)'), max_length=120, blank=True, default='')
    name_ar = models.CharField(_('Package Name (AR)'), max_length=120, blank=True, default='')

    slug = models.SlugField(_('Slug'), max_length=140, unique=True)

    tagline_en = models.CharField(_('Tagline (EN)'), max_length=200, blank=True, default='')
    tagline_fr = models.CharField(_('Tagline (FR)'), max_length=200, blank=True, default='')
    tagline_ar = models.CharField(_('Tagline (AR)'), max_length=200, blank=True, default='')

    description_en = models.TextField(_('Description (EN)'), blank=True, default='')
    description_fr = models.TextField(_('Description (FR)'), blank=True, default='')
    description_ar = models.TextField(_('Description (AR)'), blank=True, default='')

    icon_emoji = models.CharField(_('Icon / Emoji'), max_length=20, default='\U0001f680')

    price_starting_from = models.DecimalField(
        _('Starting From (MAD)'), max_digits=10, decimal_places=0,
        help_text=_('Starting price in Moroccan Dirhams. Set to 0 for "Contact Us" pricing.'),
        default=0,
    )
    price_label_en = models.CharField(_('Price Label (EN)'), max_length=60, blank=True, default='Starting from')
    price_label_fr = models.CharField(_('Price Label (FR)'), max_length=60, blank=True, default='\u00c0 partir de')
    price_label_ar = models.CharField(_('Price Label (AR)'), max_length=60, blank=True, default='\u0627\u0628\u062a\u062f\u0627\u0621\u064b \u0645\u0646')

    is_featured = models.BooleanField(_('Featured / Highlighted'), default=False, help_text=_('Highlight this as the recommended package'))
    is_active = models.BooleanField(_('Active'), default=True)
    order = models.PositiveIntegerField(_('Display Order'), default=0)

    # Pre-fill quote wizard
    prefill_project_type = models.CharField(_('Pre-fill Project Type'), max_length=50, blank=True, default='',
        help_text=_('Value to pre-fill in the quote wizard when CTA is clicked'))

    @property
    def name(self): return get_localized(self, 'name')

    @property
    def tagline(self): return get_localized(self, 'tagline')

    @property
    def description(self): return get_localized(self, 'description')

    @property
    def price_label(self): return get_localized(self, 'price_label')

    class Meta:
        verbose_name = _('Package')
        verbose_name_plural = _('Packages')
        ordering = ['order', 'pk']

    def __str__(self):
        return self.name_en or f"Package #{self.pk}"


class PackageFeature(models.Model):
    """Individual feature line items for a Package."""

    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='features')

    text_en = models.CharField(_('Feature (EN)'), max_length=200)
    text_fr = models.CharField(_('Feature (FR)'), max_length=200, blank=True, default='')
    text_ar = models.CharField(_('Feature (AR)'), max_length=200, blank=True, default='')

    is_included = models.BooleanField(_('Included'), default=True, help_text=_('If unchecked, shown as crossed out'))
    order = models.PositiveIntegerField(_('Display Order'), default=0)

    @property
    def text(self): return get_localized(self, 'text')

    class Meta:
        verbose_name = _('Package Feature')
        verbose_name_plural = _('Package Features')
        ordering = ['order', 'pk']

    def __str__(self):
        return self.text_en[:60] or f"Feature #{self.pk}"


# ── 17. Pricing Rules (Quote Calculator) ──────────────────────

class PricingRule(models.Model):
    """Admin-editable pricing rules for the quote estimator calculator."""

    CATEGORY_CHOICES = [
        ('project_type', _('Project Type Base Price')),
        ('feature', _('Feature Add-on')),
        ('pages', _('Number of Pages/Screens')),
        ('language', _('Additional Language')),
        ('timeline', _('Timeline Multiplier')),
    ]

    category = models.CharField(_('Category'), max_length=30, choices=CATEGORY_CHOICES)
    key = models.CharField(_('Key / Identifier'), max_length=80, help_text=_('e.g. "website", "ecommerce", "auth", "5-10"'))

    label_en = models.CharField(_('Label (EN)'), max_length=200)
    label_fr = models.CharField(_('Label (FR)'), max_length=200, blank=True, default='')
    label_ar = models.CharField(_('Label (AR)'), max_length=200, blank=True, default='')

    value = models.DecimalField(_('Value (MAD or multiplier)'), max_digits=10, decimal_places=2,
        help_text=_('For project_type/feature/pages/language: price in MAD. For timeline: multiplier (e.g. 1.0, 1.3, 0.9)'))

    order = models.PositiveIntegerField(_('Display Order'), default=0)
    is_active = models.BooleanField(_('Active'), default=True)

    @property
    def label(self): return get_localized(self, 'label')

    class Meta:
        verbose_name = _('Pricing Rule')
        verbose_name_plural = _('Pricing Rules')
        ordering = ['category', 'order']

    def __str__(self):
        return f"{self.get_category_display()} — {self.label_en} ({self.value})"


# ── 18. Quote Requests ────────────────────────────────────────

class QuoteRequest(models.Model):
    """Multi-step quote wizard submissions."""

    STATUS_CHOICES = [
        ('new', _('New')),
        ('contacted', _('Contacted')),
        ('proposal_sent', _('Proposal Sent')),
        ('won', _('Won')),
        ('lost', _('Lost')),
    ]

    PROJECT_TYPE_CHOICES = [
        ('website', _('Corporate Website')),
        ('ecommerce', _('E-Commerce Store')),
        ('webapp', _('Web Application / SaaS')),
        ('mobile', _('Mobile Application')),
        ('redesign', _('Website Redesign')),
        ('other', _('Other / Custom')),
    ]

    BUDGET_CHOICES = [
        ('5k-15k', '5,000 — 15,000 MAD'),
        ('15k-30k', '15,000 — 30,000 MAD'),
        ('30k-60k', '30,000 — 60,000 MAD'),
        ('60k-100k', '60,000 — 100,000 MAD'),
        ('100k+', '100,000+ MAD'),
        ('unsure', _('Not sure yet')),
    ]

    TIMELINE_CHOICES = [
        ('asap', _('ASAP (rush)')),
        ('1-2months', _('1 — 2 months')),
        ('2-4months', _('2 — 4 months')),
        ('4-6months', _('4 — 6 months')),
        ('flexible', _('Flexible')),
    ]

    # Step 1: Project info
    project_type = models.CharField(_('Project Type'), max_length=30, choices=PROJECT_TYPE_CHOICES)
    project_description = models.TextField(_('Project Description'), blank=True, default='')

    # Step 2: Features & scope
    features = models.TextField(_('Selected Features'), blank=True, default='',
        help_text=_('Comma-separated list of selected feature keys'))
    num_pages = models.CharField(_('Number of Pages/Screens'), max_length=20, blank=True, default='')
    num_languages = models.PositiveIntegerField(_('Number of Languages'), default=1)

    # Step 3: Timeline & budget
    timeline = models.CharField(_('Timeline'), max_length=20, choices=TIMELINE_CHOICES, blank=True, default='')
    budget_range = models.CharField(_('Budget Range'), max_length=20, choices=BUDGET_CHOICES, blank=True, default='')

    # Step 4: Contact info
    name = models.CharField(_('Full Name'), max_length=150)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Phone'), max_length=30, blank=True, default='')
    company = models.CharField(_('Company'), max_length=150, blank=True, default='')

    # Computed estimate
    estimated_min = models.DecimalField(_('Estimated Min (MAD)'), max_digits=10, decimal_places=0, null=True, blank=True)
    estimated_max = models.DecimalField(_('Estimated Max (MAD)'), max_digits=10, decimal_places=0, null=True, blank=True)

    # Tracking
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='new')
    source_page = models.CharField(_('Source Page'), max_length=300, blank=True, default='')
    honeypot = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    admin_notes = models.TextField(_('Admin Notes'), blank=True, default='')

    class Meta:
        verbose_name = _('Quote Request')
        verbose_name_plural = _('Quote Requests')
        ordering = ['-created_at']

    def __str__(self):
        return f"Quote #{self.pk} — {self.name} ({self.get_project_type_display()})"


# ── 19. Discovery Call Bookings ───────────────────────────────

class WeeklyAvailability(models.Model):
    """Admin-editable weekly time slots for discovery calls."""

    DAY_CHOICES = [
        (0, _('Monday')),
        (1, _('Tuesday')),
        (2, _('Wednesday')),
        (3, _('Thursday')),
        (4, _('Friday')),
        (5, _('Saturday')),
        (6, _('Sunday')),
    ]

    day_of_week = models.IntegerField(_('Day of Week'), choices=DAY_CHOICES)
    start_time = models.TimeField(_('Start Time'))
    end_time = models.TimeField(_('End Time'))
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Weekly Availability Slot')
        verbose_name_plural = _('Weekly Availability')
        ordering = ['day_of_week', 'start_time']
        unique_together = [['day_of_week', 'start_time', 'end_time']]

    def __str__(self):
        return f"{self.get_day_of_week_display()} {self.start_time.strftime('%H:%M')} — {self.end_time.strftime('%H:%M')}"


class Booking(models.Model):
    """Discovery call booking submissions."""

    STATUS_CHOICES = [
        ('new', _('New / Confirmed')),
        ('contacted', _('Contacted')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
        ('no_show', _('No Show')),
    ]

    name = models.CharField(_('Full Name'), max_length=150)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Phone'), max_length=30, blank=True, default='')
    company = models.CharField(_('Company'), max_length=150, blank=True, default='')

    date = models.DateField(_('Booking Date'))
    time_slot = models.TimeField(_('Time Slot'))
    timezone_name = models.CharField(_('Visitor Timezone'), max_length=60, blank=True, default='')

    message = models.TextField(_('Project Brief'), blank=True, default='')

    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='new')
    source_page = models.CharField(_('Source Page'), max_length=300, blank=True, default='')
    honeypot = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    admin_notes = models.TextField(_('Admin Notes'), blank=True, default='')

    class Meta:
        verbose_name = _('Discovery Call Booking')
        verbose_name_plural = _('Discovery Call Bookings')
        ordering = ['-date', '-time_slot']
        unique_together = [['date', 'time_slot']]

    def __str__(self):
        return f"Booking #{self.pk} — {self.name} on {self.date} at {self.time_slot}"

    @property
    def google_calendar_url(self):
        """Generate an 'Add to Google Calendar' link."""
        import datetime
        start_dt = datetime.datetime.combine(self.date, self.time_slot)
        end_dt = start_dt + datetime.timedelta(minutes=30)
        fmt = '%Y%m%dT%H%M%S'
        return (
            f"https://calendar.google.com/calendar/render?action=TEMPLATE"
            f"&text=getNexiro+Discovery+Call"
            f"&dates={start_dt.strftime(fmt)}/{end_dt.strftime(fmt)}"
            f"&details=Discovery+call+with+getNexiro+team"
            f"&location=Video+Call"
        )


# ── 20. Lead Magnet Subscribers ───────────────────────────────

class Subscriber(models.Model):
    """Email subscribers for lead magnets (checklist downloads, newsletter)."""

    STATUS_CHOICES = [
        ('pending', _('Pending Confirmation')),
        ('confirmed', _('Confirmed')),
        ('unsubscribed', _('Unsubscribed')),
    ]

    email = models.EmailField(_('Email'), unique=True)
    name = models.CharField(_('Name'), max_length=150, blank=True, default='')
    consent = models.BooleanField(_('Marketing Consent'), default=False)
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='confirmed')

    lead_magnet = models.CharField(_('Lead Magnet'), max_length=100, blank=True, default='checklist',
        help_text=_('Which resource they downloaded'))

    source_page = models.CharField(_('Source Page'), max_length=300, blank=True, default='')
    honeypot = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(_('Subscribed At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Subscriber')
        verbose_name_plural = _('Subscribers')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} ({self.get_status_display()})"
