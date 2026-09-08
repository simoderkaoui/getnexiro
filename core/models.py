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
    return getattr(instance, field_name, '')


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

    # Localized Property Getters
    @property
    def tagline(self): return get_localized(self, 'tagline')

    @property
    def hero_title(self): return get_localized(self, 'hero_title')

    @property
    def hero_subtitle(self): return get_localized(self, 'hero_subtitle')

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

    description_en = models.TextField(_('Description (EN)'))
    description_fr = models.TextField(_('Description (FR)'), blank=True, default='')
    description_ar = models.TextField(_('Description (AR)'), blank=True, default='')

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
    def description(self): return get_localized(self, 'description')

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['order', 'pk']

    def __str__(self):
        return self.title_en or self.title_ar or f"Service #{self.pk}"


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

    category = models.ForeignKey(
        ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name=_('Category'),
    )

    description_en = models.TextField(_('Description (EN)'))
    description_fr = models.TextField(_('Description (FR)'), blank=True, default='')
    description_ar = models.TextField(_('Description (AR)'), blank=True, default='')

    image = models.ImageField(
        _('Cover Image'), upload_to='projects/', blank=True, null=True,
    )
    client_name = models.CharField(_('Client Name'), max_length=100, blank=True)
    technologies = models.CharField(_('Technologies'), max_length=300, blank=True)
    is_featured = models.BooleanField(_('Featured on Home Page'), default=False)
    order = models.PositiveIntegerField(_('Display Order'), default=0)
    created_at = models.DateField(_('Project Date'), auto_now_add=True)

    @property
    def title(self): return get_localized(self, 'title')

    @property
    def description(self): return get_localized(self, 'description')

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title_en or self.title_ar or f"Project #{self.pk}"


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
