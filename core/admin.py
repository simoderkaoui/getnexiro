"""
getNexiro — Admin Configuration with Multilingual Support.

Clean, organized admin dashboard for managing EN / FR / AR content.
"""

from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import (
    SiteConfig, Service, ServiceSolution, ProjectCategory, Project, ProjectImage,
    TeamMember, Testimonial, ClientLogo, Stat, ContactMessage,
    CompanyValue, ProcessStep, StoreItem, BlogCategory, BlogPost, Author,
    LegalPage, FAQ,
    Package, PackageFeature, PricingRule, QuoteRequest,
    WeeklyAvailability, Booking, Subscriber,
    CityServicePage,
)
import csv
from django.http import HttpResponse


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    save_on_top = True
    fieldsets = (
        (_('Brand Identity & Logo'), {
            'fields': ('site_name', 'site_logo', 'site_favicon', 'email', 'phone'),
            'description': _('Configure site name, header logo, browser favicon, and primary contact info.'),
        }),
        (_('Hero Background (Video / Wallpaper)'), {
            'fields': ('hero_bg_type', 'hero_bg_image', 'hero_bg_video', 'hero_bg_video_url'),
            'description': _('Choose whether to display the animated glow mesh, a custom wallpaper picture, or a looping background video (MP4 file or direct URL).'),
        }),
        (_('Page Header Background Videos (Per Page)'), {
            'fields': (
                ('about_bg_video', 'about_bg_video_url'),
                ('services_bg_video', 'services_bg_video_url'),
                ('projects_bg_video', 'projects_bg_video_url'),
                ('blog_bg_video', 'blog_bg_video_url'),
                ('contact_bg_video', 'contact_bg_video_url'),
            ),
            'description': _('Upload an MP4/WebM video file or enter a direct video URL for each page header. If left empty, the site default video will be used.'),
        }),
        (_('Hero Badge (Multilingual)'), {
            'fields': ('hero_badge_en', 'hero_badge_fr', 'hero_badge_ar'),
        }),
        (_('Hero Headline (Multilingual)'), {
            'fields': ('hero_title_en', 'hero_title_fr', 'hero_title_ar'),
        }),
        (_('Hero Subtitle (Multilingual)'), {
            'fields': ('hero_subtitle_en', 'hero_subtitle_fr', 'hero_subtitle_ar'),
        }),
        (_('Hero CTA Buttons (Multilingual)'), {
            'fields': (
                'hero_cta_primary_text_en', 'hero_cta_primary_text_fr', 'hero_cta_primary_text_ar',
                'hero_cta_secondary_text_en', 'hero_cta_secondary_text_fr', 'hero_cta_secondary_text_ar',
            ),
        }),
        (_('Tagline (Multilingual)'), {
            'fields': ('tagline_en', 'tagline_fr', 'tagline_ar'),
        }),
        (_('About Us Picture & Story'), {
            'fields': ('about_image', 'about_text_en', 'about_text_fr', 'about_text_ar'),
            'description': _('Upload feature picture for About page and edit story in all languages.'),
        }),
        (_('Mission Statement (Multilingual)'), {
            'fields': ('mission_statement_en', 'mission_statement_fr', 'mission_statement_ar'),
        }),
        (_('Global Call-To-Action Banner (Multilingual)'), {
            'fields': (
                'cta_title_en', 'cta_title_fr', 'cta_title_ar',
                'cta_subtitle_en', 'cta_subtitle_fr', 'cta_subtitle_ar',
                'cta_button_text_en', 'cta_button_text_fr', 'cta_button_text_ar',
            ),
        }),
        (_('Address & Location'), {
            'fields': (
                'address_en', 'address_fr', 'address_ar',
                'address_detail_en', 'address_detail_fr', 'address_detail_ar',
                'map_embed_url',
            ),
        }),
        (_('Business Hours'), {
            'fields': ('business_hours_en', 'business_hours_fr', 'business_hours_ar'),
        }),
        (_('SEO Meta Descriptions'), {
            'fields': ('meta_description_en', 'meta_description_fr', 'meta_description_ar'),
        }),
        (_('Social Links'), {
            'fields': ('instagram_url', 'linkedin_url', 'github_url', 'twitter_url'),
        }),
        (_('Page-Level SEO Titles (Multilingual)'), {
            'fields': (
                'default_og_image',
                'home_seo_title_en', 'home_seo_title_fr', 'home_seo_title_ar',
                'home_seo_description_en', 'home_seo_description_fr', 'home_seo_description_ar',
                'about_seo_title_en', 'about_seo_title_fr', 'about_seo_title_ar',
                'about_seo_description_en', 'about_seo_description_fr', 'about_seo_description_ar',
                'services_seo_title_en', 'services_seo_title_fr', 'services_seo_title_ar',
                'services_seo_description_en', 'services_seo_description_fr', 'services_seo_description_ar',
                'projects_seo_title_en', 'projects_seo_title_fr', 'projects_seo_title_ar',
                'projects_seo_description_en', 'projects_seo_description_fr', 'projects_seo_description_ar',
                'blog_seo_title_en', 'blog_seo_title_fr', 'blog_seo_title_ar',
                'blog_seo_description_en', 'blog_seo_description_fr', 'blog_seo_description_ar',
                'contact_seo_title_en', 'contact_seo_title_fr', 'contact_seo_title_ar',
                'contact_seo_description_en', 'contact_seo_description_fr', 'contact_seo_description_ar',
                'packages_seo_title_en', 'packages_seo_title_fr', 'packages_seo_title_ar',
                'packages_seo_description_en', 'packages_seo_description_fr', 'packages_seo_description_ar',
            ),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class ServiceSolutionInline(admin.TabularInline):
    model = ServiceSolution
    extra = 2
    fields = ('icon_emoji', 'title_en', 'title_fr', 'title_ar', 'description_en', 'description_fr', 'description_ar', 'order')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title_en', 'slug', 'icon', 'is_featured', 'order')
    list_filter = ('is_featured', 'icon')
    list_editable = ('is_featured', 'order')
    search_fields = ('title_en', 'title_fr', 'title_ar', 'description_en', 'slug')
    prepopulated_fields = {'slug': ('title_en',)}
    ordering = ('order',)
    inlines = [ServiceSolutionInline]

    fieldsets = (
        (_('Titles & Slug (Multilingual)'), {
            'fields': ('title_en', 'title_fr', 'title_ar', 'slug'),
        }),
        (_('Tagline / Subtitle (Multilingual)'), {
            'fields': ('subtitle_en', 'subtitle_fr', 'subtitle_ar'),
        }),
        (_('Overview (Multilingual)'), {
            'fields': ('description_en', 'description_fr', 'description_ar'),
        }),
        (_('Engineering Methodology (Multilingual)'), {
            'fields': ('methodology_en', 'methodology_fr', 'methodology_ar'),
            'classes': ('collapse',),
        }),
        (_('Core Deliverables (Multilingual)'), {
            'fields': ('deliverables_en', 'deliverables_fr', 'deliverables_ar'),
            'classes': ('collapse',),
        }),
        (_('Technologies & Timeline'), {
            'fields': ('technologies', 'timeline'),
        }),
        (_('Configuration'), {
            'fields': ('icon', 'is_featured', 'order'),
        }),
        (_('SEO Overrides'), {
            'fields': ('noindex', 'seo_title_en', 'seo_title_fr', 'seo_title_ar',
                       'seo_description_en', 'seo_description_fr', 'seo_description_ar', 'og_image'),
            'classes': ('collapse',),
        }),
    )


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_fr', 'name_ar', 'slug')
    prepopulated_fields = {'slug': ('name_en',)}


class SafeProjectImageFormSet(BaseInlineFormSet):
    """
    Guarantees formset integrity. If the browser or proxy drops
    the inline management form fields during upload, safely treats
    the formset as untouched to prevent the form from crashing.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_objects = []
        self.changed_objects = []
        self.deleted_objects = []
        if self.is_bound and (not self.data or f'{self.prefix}-TOTAL_FORMS' not in self.data):
            self.data = self.data.copy() if self.data is not None else {}
            self.data[f'{self.prefix}-TOTAL_FORMS'] = '0'
            self.data[f'{self.prefix}-INITIAL_FORMS'] = '0'
            self.data[f'{self.prefix}-MIN_NUM_FORMS'] = '0'
            self.data[f'{self.prefix}-MAX_NUM_FORMS'] = '1000'
            self._has_synthesized_management = True
        else:
            self._has_synthesized_management = False

    def full_clean(self):
        if self.is_bound and (not self.data or f'{self.prefix}-TOTAL_FORMS' not in self.data):
            self.data = self.data.copy() if self.data is not None else {}
            self.data[f'{self.prefix}-TOTAL_FORMS'] = '0'
            self.data[f'{self.prefix}-INITIAL_FORMS'] = '0'
            self.data[f'{self.prefix}-MIN_NUM_FORMS'] = '0'
            self.data[f'{self.prefix}-MAX_NUM_FORMS'] = '1000'
            self._has_synthesized_management = True
        return super().full_clean()

    def save(self, commit=True):
        self.new_objects = getattr(self, 'new_objects', [])
        self.changed_objects = getattr(self, 'changed_objects', [])
        self.deleted_objects = getattr(self, 'deleted_objects', [])
        if getattr(self, '_has_synthesized_management', False):
            return []
        return super().save(commit=commit)


class ProjectImageInline(admin.StackedInline):
    model = ProjectImage
    formset = SafeProjectImageFormSet
    extra = 1
    verbose_name = _('Project Gallery Carousel Photo')
    verbose_name_plural = _('📸 Project Gallery Carousel Photos (Upload & Manage Showcase Slides)')
    fields = (('image', 'image_preview'), ('caption_en', 'caption_fr', 'caption_ar'), 'order')
    readonly_fields = ('image_preview',)

    @admin.display(description=_('Current Photo Preview'))
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<div style="margin-top:6px;"><img src="{}" style="max-height:90px; max-width:180px; border-radius:8px; border:1px solid rgba(255,255,255,0.15); object-fit:cover; box-shadow:0 4px 12px rgba(0,0,0,0.3);" /></div>',
                obj.image.url
            )
        return '—'


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'image_preview', 'caption_en', 'caption_fr', 'caption_ar', 'order')
    list_filter = ('project',)
    search_fields = ('project__title_en', 'caption_en', 'caption_fr', 'caption_ar')
    ordering = ('project', 'order')

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        project_id = request.GET.get('project')
        if project_id:
            initial['project'] = project_id
        return initial

    @admin.display(description=_('Preview'))
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:45px; border-radius:6px; object-fit:cover;" />', obj.image.url)
        return '—'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title_en', 'category', 'is_featured', 'image_preview', 'gallery_count', 'order')
    list_filter = ('category', 'is_featured')
    list_editable = ('is_featured', 'order')
    search_fields = ('title_en', 'title_fr', 'title_ar', 'description_en', 'slug')
    prepopulated_fields = {'slug': ('title_en',)}
    ordering = ('order',)
    readonly_fields = ('gallery_manager_shortcut',)
    inlines = [ProjectImageInline]

    fieldsets = (
        (_('Titles & Slug (Multilingual)'), {
            'fields': ('title_en', 'title_fr', 'title_ar', 'slug'),
        }),
        (_('Category, Client, Cover Image & Gallery'), {
            'fields': (
                'category', 'client_name', 'technologies', 'duration', 'year', 'live_url', 'github_url',
                'image', 'gallery_manager_shortcut'
            ),
            'description': _('Upload the primary cover image below, or use the Gallery manager to add multiple carousel slides to this case study.'),
        }),
        (_('Executive Overview (Multilingual)'), {
            'fields': ('description_en', 'description_fr', 'description_ar'),
        }),
        (_('Deep-Dive: The Challenge (Multilingual)'), {
            'fields': ('challenge_en', 'challenge_fr', 'challenge_ar'),
            'classes': ('collapse',),
        }),
        (_('Deep-Dive: Architecture & Solution (Multilingual)'), {
            'fields': ('solution_en', 'solution_fr', 'solution_ar'),
            'classes': ('collapse',),
        }),
        (_('Deep-Dive: Results & Impact (Multilingual)'), {
            'fields': ('results_en', 'results_fr', 'results_ar'),
            'classes': ('collapse',),
        }),
        (_('Client Testimonial & Feedback (Multilingual)'), {
            'fields': (
                'client_feedback_quote_en', 'client_feedback_quote_fr', 'client_feedback_quote_ar',
                'client_feedback_author', 'client_feedback_role',
            ),
            'classes': ('collapse',),
        }),
        (_('Settings'), {
            'fields': ('is_featured', 'order'),
        }),
        (_('SEO Overrides'), {
            'fields': ('noindex', 'seo_title_en', 'seo_title_fr', 'seo_title_ar',
                       'seo_description_en', 'seo_description_fr', 'seo_description_ar', 'og_image'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description=_('Preview'))
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:36px; border-radius:6px; object-fit:cover;" />', obj.image.url)
        return '—'

    @admin.display(description=_('Gallery Photos'))
    def gallery_count(self, obj):
        count = obj.gallery_images.count()
        list_url = f"/admin/core/projectimage/?project__id__exact={obj.id}"
        add_url = f"/admin/core/projectimage/add/?project={obj.id}"
        if count > 0:
            return format_html(
                '<a href="{}" style="font-weight:600; color:#38bdf8; text-decoration:underline;">📷 {} photo{}</a> '
                '<a href="{}" style="margin-left:6px; padding:2px 7px; background:#0284c7; color:#fff; border-radius:4px; font-size:11px; text-decoration:none;">+ Add</a>',
                list_url, count, 's' if count != 1 else '', add_url
            )
        return format_html(
            '<span style="color:#64748b;">0 photos</span> '
            '<a href="{}" style="margin-left:6px; padding:2px 7px; background:#0284c7; color:#fff; border-radius:4px; font-size:11px; text-decoration:none;">+ Add Photo</a>',
            add_url
        )

    @admin.display(description=_('📸 Project Gallery Carousel'))
    def gallery_manager_shortcut(self, obj):
        if not obj or not obj.pk:
            return _("Save this project first to add gallery carousel photos.")
        count = obj.gallery_images.count()
        add_url = f"/admin/core/projectimage/add/?project={obj.id}"
        list_url = f"/admin/core/projectimage/?project__id__exact={obj.id}"
        return format_html(
            '<div style="background:linear-gradient(135deg, rgba(2,132,199,0.18) 0%, rgba(56,189,248,0.08) 100%); '
            'border:1px solid rgba(56,189,248,0.35); border-radius:10px; padding:14px 18px; margin:6px 0 14px;">'
            '<div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">'
            '<div>'
            '<span style="font-size:14px; font-weight:700; color:#38bdf8;">📸 Carousel Photo Gallery</span>'
            '<p style="margin:4px 0 0; color:#cbd5e1; font-size:13px;">This project currently has <strong>{} photo{}</strong> in its interactive carousel.</p>'
            '</div>'
            '<div style="display:flex; gap:8px;">'
            '<a href="{}" target="_blank" style="background:#0284c7; color:#ffffff; font-weight:600; padding:6px 14px; border-radius:6px; text-decoration:none; display:inline-flex; align-items:center; font-size:13px; box-shadow:0 2px 6px rgba(2,132,199,0.4);">'
            '+ Upload Photo Directly ↗'
            '</a>'
            '<a href="{}" target="_blank" style="background:rgba(255,255,255,0.08); color:#38bdf8; border:1px solid rgba(56,189,248,0.3); font-weight:500; padding:6px 14px; border-radius:6px; text-decoration:none; font-size:13px;">'
            'View All Gallery Photos ({}) ↗'
            '</a>'
            '</div>'
            '</div>'
            '<p style="margin:10px 0 0; color:#94a3b8; font-size:12px; border-top:1px solid rgba(255,255,255,0.08); padding-top:8px;">'
            '💡 <em>Tip: You can upload photos directly using the button above, or scroll down to the bottom of this form to upload slides in bulk.</em>'
            '</p>'
            '</div>',
            count, 's' if count != 1 else '', add_url, list_url, count
        )



@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role_en', 'role_fr', 'role_ar', 'photo_preview', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'role_en', 'role_ar')
    ordering = ('order',)

    fieldsets = (
        (_('Personal Info'), {
            'fields': ('name', 'photo', 'linkedin_url', 'order'),
        }),
        (_('Roles (Multilingual)'), {
            'fields': ('role_en', 'role_fr', 'role_ar'),
        }),
        (_('Bios (Multilingual)'), {
            'fields': ('bio_en', 'bio_fr', 'bio_ar'),
        }),
    )

    @admin.display(description=_('Photo'))
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:36px; width:36px; border-radius:50%; object-fit:cover;" />', obj.photo.url)
        return '—'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'company', 'author_role_en', 'is_verified', 'is_featured', 'order')
    list_filter = ('is_verified', 'is_featured')
    list_editable = ('is_verified', 'is_featured', 'order')
    search_fields = ('author_name', 'company', 'quote_en', 'quote_ar')
    ordering = ('order',)

    fieldsets = (
        (_('Author Info'), {
            'fields': ('author_name', 'company', 'avatar', 'is_verified', 'is_featured', 'order'),
        }),
        (_('Roles (Multilingual)'), {
            'fields': ('author_role_en', 'author_role_fr', 'author_role_ar'),
        }),
        (_('Quotes (Multilingual)'), {
            'fields': ('quote_en', 'quote_fr', 'quote_ar'),
        }),
    )


@admin.register(ClientLogo)
class ClientLogoAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview', 'order')
    list_editable = ('order',)
    ordering = ('order',)

    @admin.display(description=_('Logo'))
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:28px; object-fit:contain;" />', obj.logo.url)
        return '—'


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('value', 'label_en', 'label_fr', 'label_ar', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    list_editable = ('is_read',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False


@admin.register(CompanyValue)
class CompanyValueAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'title_fr', 'title_ar', 'icon', 'order')
    list_editable = ('order',)
    search_fields = ('title_en', 'title_fr', 'title_ar', 'description_en')
    ordering = ('order',)

    fieldsets = (
        (_('Titles (Multilingual)'), {
            'fields': ('title_en', 'title_fr', 'title_ar'),
        }),
        (_('Descriptions (Multilingual)'), {
            'fields': ('description_en', 'description_fr', 'description_ar'),
        }),
        (_('Appearance'), {
            'fields': ('icon', 'order'),
        }),
    )


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title_en', 'title_fr', 'title_ar', 'tags', 'order')
    list_editable = ('order',)
    search_fields = ('title_en', 'title_fr', 'title_ar', 'tags')
    ordering = ('order',)

    fieldsets = (
        (_('Step Info'), {
            'fields': ('step_number', 'tags', 'order'),
        }),
        (_('Titles (Multilingual)'), {
            'fields': ('title_en', 'title_fr', 'title_ar'),
        }),
        (_('Descriptions (Multilingual)'), {
            'fields': ('description_en', 'description_fr', 'description_ar'),
        }),
    )


@admin.register(StoreItem)
class StoreItemAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'title_fr', 'title_ar', 'emoji', 'badge_en', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title_en', 'title_fr', 'title_ar')
    ordering = ('order',)

    fieldsets = (
        (_('Item Settings'), {
            'fields': ('emoji', 'is_active', 'order'),
        }),
        (_('Titles (Multilingual)'), {
            'fields': ('title_en', 'title_fr', 'title_ar'),
        }),
        (_('Descriptions (Multilingual)'), {
            'fields': ('description_en', 'description_fr', 'description_ar'),
        }),
        (_('Badges (Multilingual)'), {
            'fields': ('badge_en', 'badge_fr', 'badge_ar'),
        }),
    )

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_fr', 'name_ar', 'slug')
    prepopulated_fields = {'slug': ('name_en',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'role_en', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'role_en', 'bio_en')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('image_preview_list', 'title_en', 'category', 'author', 'status', 'noindex', 'index_in_sitemap', 'is_featured', 'published_at')
    list_display_links = ('title_en',)
    list_filter = ('status', 'noindex', 'index_in_sitemap', 'is_featured', 'category')
    list_editable = ('status', 'noindex', 'index_in_sitemap', 'is_featured')
    search_fields = ('title_en', 'title_fr', 'title_ar', 'body_en', 'slug', 'tags')
    prepopulated_fields = {'slug': ('title_en',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at', '-created_at')
    readonly_fields = ('image_preview',)

    fieldsets = (
        (_('Title & Slug'), {
            'fields': ('title_en', 'title_fr', 'title_ar', 'slug'),
        }),
        (_('Featured Cover Image & Media'), {
            'fields': ('featured_image', 'image_preview', 'featured_image_alt', 'category', 'tags'),
            'description': _('Upload the main article cover photo here (1200x630 recommended).'),
        }),
        (_('Excerpt / Summary (Multilingual)'), {
            'fields': ('excerpt_en', 'excerpt_fr', 'excerpt_ar'),
        }),
        (_('Body (Multilingual)'), {
            'fields': ('body_en', 'body_fr', 'body_ar'),
        }),
        (_('SEO Meta & Indexation'), {
            'fields': ('noindex', 'index_in_sitemap',
                       'meta_title_en', 'meta_title_fr', 'meta_title_ar',
                       'meta_description_en', 'meta_description_fr', 'meta_description_ar',
                       'meta_keywords'),
        }),
        (_('Author & Reading'), {
            'fields': ('author', 'author_name', 'reading_time_minutes'),
        }),
        (_('Publishing'), {
            'fields': ('status', 'is_featured', 'published_at'),
        }),
    )

    def image_preview(self, obj):
        if obj and obj.featured_image:
            from django.utils.html import format_html
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" style="max-height: 120px; max-width: 240px; border-radius: 8px; border: 1px solid rgba(56,189,248,0.4);" /></a>',
                obj.featured_image.url
            )
        return _('No image uploaded yet')
    image_preview.short_description = _('Current Image Preview')

    def image_preview_list(self, obj):
        if obj and obj.featured_image:
            from django.utils.html import format_html
            return format_html(
                '<img src="{0}" style="width: 44px; height: 32px; object-fit: cover; border-radius: 4px;" />',
                obj.featured_image.url
            )
        return '-'
    image_preview_list.short_description = _('Cover')




@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title_en', 'title_fr', 'title_ar', 'updated_at')
    search_fields = ('title_en', 'title_fr', 'title_ar', 'body_en')

    fieldsets = (
        (_('Page Identifier'), {
            'fields': ('slug',),
        }),
        (_('Title (Multilingual)'), {
            'fields': ('title_en', 'title_fr', 'title_ar'),
        }),
        (_('Content (Multilingual)'), {
            'fields': ('body_en', 'body_fr', 'body_ar'),
            'description': _('HTML is allowed. Use <h2>, <h3>, <p>, <ul>, <li> tags for structure.'),
        }),
        (_('SEO Overrides'), {
            'fields': ('noindex', 'seo_title_en', 'seo_title_fr', 'seo_title_ar',
                       'seo_description_en', 'seo_description_fr', 'seo_description_ar', 'og_image'),
            'classes': ('collapse',),
        }),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question_en', 'section', 'is_active', 'order')
    list_filter = ('section', 'is_active')
    list_editable = ('section', 'is_active', 'order')
    search_fields = ('question_en', 'question_fr', 'question_ar', 'answer_en')
    ordering = ('section', 'order')

    fieldsets = (
        (_('Question (Multilingual)'), {
            'fields': ('question_en', 'question_fr', 'question_ar'),
        }),
        (_('Answer (Multilingual)'), {
            'fields': ('answer_en', 'answer_fr', 'answer_ar'),
        }),
        (_('Settings'), {
            'fields': ('section', 'order', 'is_active'),
        }),
    )



# ══════════════════════════════════════════════════════════════
# PHASE 2: Lead Generation Admin
# ══════════════════════════════════════════════════════════════

def export_as_csv(modeladmin, request, queryset):
    """Generic CSV export admin action."""
    meta = modeladmin.model._meta
    field_names = [f.name for f in meta.fields]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural.replace(" ", "_")}.csv'
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, f) for f in field_names])
    return response
export_as_csv.short_description = _('Export selected as CSV')


class PackageFeatureInline(admin.TabularInline):
    model = PackageFeature
    extra = 3
    fields = ('text_en', 'text_fr', 'text_ar', 'is_included', 'order')


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name_en', 'price_starting_from', 'is_featured', 'is_active', 'order')
    list_filter = ('is_featured', 'is_active')
    list_editable = ('is_featured', 'is_active', 'order')
    prepopulated_fields = {'slug': ('name_en',)}
    ordering = ('order',)
    inlines = [PackageFeatureInline]

    fieldsets = (
        (_('Package Name (Multilingual)'), {
            'fields': ('name_en', 'name_fr', 'name_ar', 'slug'),
        }),
        (_('Tagline (Multilingual)'), {
            'fields': ('tagline_en', 'tagline_fr', 'tagline_ar'),
        }),
        (_('Description (Multilingual)'), {
            'fields': ('description_en', 'description_fr', 'description_ar'),
        }),
        (_('Pricing'), {
            'fields': ('price_starting_from', 'price_label_en', 'price_label_fr', 'price_label_ar'),
        }),
        (_('Configuration'), {
            'fields': ('icon_emoji', 'is_featured', 'is_active', 'order', 'prefill_project_type'),
        }),
        (_('SEO Overrides'), {
            'fields': ('noindex', 'seo_title_en', 'seo_title_fr', 'seo_title_ar',
                       'seo_description_en', 'seo_description_fr', 'seo_description_ar', 'og_image'),
            'classes': ('collapse',),
        }),
    )


@admin.register(PricingRule)
class PricingRuleAdmin(admin.ModelAdmin):
    list_display = ('label_en', 'category', 'key', 'value', 'is_active', 'order')
    list_filter = ('category', 'is_active')
    list_editable = ('value', 'is_active', 'order')
    search_fields = ('label_en', 'key')
    ordering = ('category', 'order')

    fieldsets = (
        (_('Rule Settings'), {
            'fields': ('category', 'key', 'value', 'is_active', 'order'),
        }),
        (_('Label (Multilingual)'), {
            'fields': ('label_en', 'label_fr', 'label_ar'),
        }),
    )


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'project_type', 'budget_range', 'timeline', 'status', 'created_at')
    list_filter = ('status', 'project_type', 'budget_range', 'created_at')
    list_editable = ('status',)
    search_fields = ('name', 'email', 'company', 'project_description')
    readonly_fields = ('name', 'email', 'phone', 'company', 'project_type', 'project_description',
                       'features', 'num_pages', 'num_languages', 'timeline', 'budget_range',
                       'estimated_min', 'estimated_max', 'source_page', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    actions = [export_as_csv]

    fieldsets = (
        (_('Contact Info'), {
            'fields': ('name', 'email', 'phone', 'company'),
        }),
        (_('Project Details'), {
            'fields': ('project_type', 'project_description', 'features', 'num_pages', 'num_languages'),
        }),
        (_('Budget & Timeline'), {
            'fields': ('timeline', 'budget_range', 'estimated_min', 'estimated_max'),
        }),
        (_('Status & Notes'), {
            'fields': ('status', 'admin_notes', 'source_page', 'created_at', 'updated_at'),
        }),
    )

    def has_add_permission(self, request):
        return False


@admin.register(WeeklyAvailability)
class WeeklyAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('get_day_of_week_display', 'start_time', 'end_time', 'is_active')
    list_filter = ('day_of_week', 'is_active')
    list_editable = ('is_active',)
    ordering = ('day_of_week', 'start_time')

    @admin.display(description=_('Day'))
    def get_day_of_week_display(self, obj):
        return obj.get_day_of_week_display()


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date', 'time_slot', 'status', 'created_at')
    list_filter = ('status', 'date', 'created_at')
    list_editable = ('status',)
    search_fields = ('name', 'email', 'company', 'message')
    readonly_fields = ('name', 'email', 'phone', 'company', 'date', 'time_slot',
                       'timezone_name', 'message', 'source_page', 'created_at')
    date_hierarchy = 'date'
    ordering = ('-date', '-time_slot')
    actions = [export_as_csv]

    fieldsets = (
        (_('Contact Info'), {
            'fields': ('name', 'email', 'phone', 'company'),
        }),
        (_('Booking Details'), {
            'fields': ('date', 'time_slot', 'timezone_name', 'message'),
        }),
        (_('Status & Notes'), {
            'fields': ('status', 'admin_notes', 'source_page', 'created_at'),
        }),
    )

    def has_add_permission(self, request):
        return False


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'language', 'is_confirmed', 'status', 'source', 'lead_magnet', 'created_at', 'unsubscribed_at')
    list_filter = ('is_confirmed', 'status', 'language', 'source', 'lead_magnet', 'consent', 'created_at')
    list_editable = ('status', 'is_confirmed')
    search_fields = ('email', 'name', 'source', 'source_page')
    readonly_fields = ('created_at', 'unsubscribed_at', 'confirmation_token', 'token_created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    actions = [export_as_csv]

    def has_add_permission(self, request):
        return True




@admin.register(CityServicePage)
class CityServicePageAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('__str__', 'city', 'service', 'is_published', 'updated_at')
    list_filter = ('is_published', 'city', 'service')
    list_editable = ('is_published',)
    search_fields = ('h1_en', 'h1_fr', 'h1_ar', 'slug')
    prepopulated_fields = {'slug': ('h1_en',)}
    ordering = ('service', 'city')

    fieldsets = (
        (_('Service & City'), {
            'fields': ('service', 'city', 'slug', 'is_published'),
        }),
        (_('H1 Title (Multilingual)'), {
            'fields': ('h1_en', 'h1_fr', 'h1_ar'),
        }),
        (_('Intro Paragraph (Multilingual)'), {
            'fields': ('intro_en', 'intro_fr', 'intro_ar'),
        }),
        (_('Main Body (Multilingual)'), {
            'fields': ('body_en', 'body_fr', 'body_ar'),
        }),
        (_('Why Choose Us (Multilingual)'), {
            'fields': ('why_choose_us_en', 'why_choose_us_fr', 'why_choose_us_ar'),
            'classes': ('collapse',),
        }),
        (_('Local Industries (Multilingual)'), {
            'fields': ('industries_served_en', 'industries_served_fr', 'industries_served_ar'),
            'classes': ('collapse',),
        }),
        (_('SEO Overrides'), {
            'fields': ('noindex', 'seo_title_en', 'seo_title_fr', 'seo_title_ar',
                       'seo_description_en', 'seo_description_fr', 'seo_description_ar', 'og_image'),
            'classes': ('collapse',),
        }),
    )





# ── Admin Dashboard Summary ──────────────────────────────────────
import datetime as _dt
from django.contrib.admin import AdminSite as _OrigAdminSite

class NexiroAdminSite(_OrigAdminSite):
    site_header = 'getNexiro Admin'
    site_title = 'getNexiro Dashboard'
    index_title = 'Content Management'

    def each_context(self, request):
        ctx = super().each_context(request)
        try:
            from core.models import QuoteRequest, Booking, Subscriber, ContactMessage, Service
            today = _dt.date.today()
            ctx['new_quotes'] = QuoteRequest.objects.filter(status='new').count()
            ctx['upcoming_bookings'] = Booking.objects.filter(
                date__gte=today, status='new'
            ).count()
            ctx['confirmed_subscribers'] = Subscriber.objects.filter(status='confirmed').count()
            ctx['pending_subscribers'] = Subscriber.objects.filter(status='pending').count()
            ctx['unread_messages'] = ContactMessage.objects.filter(is_read=False).count()
            ctx['total_services'] = Service.objects.count()
        except Exception:
            pass
        return ctx

nexiro_admin = NexiroAdminSite(name='admin')


# Copy all registrations from default admin.site to nexiro_admin
for model, model_admin in admin.site._registry.copy().items():
    try:
        nexiro_admin.register(model, type(model_admin))
    except admin.sites.AlreadyRegistered:
        pass
