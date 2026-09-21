"""
getNexiro — Admin Configuration with Multilingual Support.

Clean, organized admin dashboard for managing EN / FR / AR content.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import (
    SiteConfig, Service, ServiceSolution, ProjectCategory, Project, ProjectImage,
    TeamMember, Testimonial, ClientLogo, Stat, ContactMessage,
    CompanyValue, ProcessStep, StoreItem, BlogCategory, BlogPost,
)


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
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
    )


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_fr', 'name_ar', 'slug')
    prepopulated_fields = {'slug': ('name_en',)}


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 2
    fields = ('image', 'caption_en', 'caption_fr', 'caption_ar', 'order', 'image_preview')
    readonly_fields = ('image_preview',)

    @admin.display(description=_('Preview'))
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:45px; border-radius:6px; object-fit:cover;" />', obj.image.url)
        return '—'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'category', 'is_featured', 'image_preview', 'gallery_count', 'order')
    list_filter = ('category', 'is_featured')
    list_editable = ('is_featured', 'order')
    search_fields = ('title_en', 'title_fr', 'title_ar', 'description_en', 'slug')
    prepopulated_fields = {'slug': ('title_en',)}
    ordering = ('order',)
    inlines = [ProjectImageInline]

    fieldsets = (
        (_('Titles & Slug (Multilingual)'), {
            'fields': ('title_en', 'title_fr', 'title_ar', 'slug'),
        }),
        (_('Category, Client & Links'), {
            'fields': ('category', 'client_name', 'technologies', 'duration', 'year', 'live_url', 'github_url', 'image'),
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
    )

    @admin.display(description=_('Preview'))
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:36px; border-radius:6px; object-fit:cover;" />', obj.image.url)
        return '—'

    @admin.display(description=_('Gallery'))
    def gallery_count(self, obj):
        count = obj.gallery_images.count()
        return f"{count} photo{'s' if count != 1 else ''}"



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
    list_display = ('author_name', 'company', 'author_role_en', 'is_featured', 'order')
    list_filter = ('is_featured',)
    list_editable = ('is_featured', 'order')
    search_fields = ('author_name', 'company', 'quote_en', 'quote_ar')
    ordering = ('order',)

    fieldsets = (
        (_('Author Info'), {
            'fields': ('author_name', 'company', 'avatar', 'is_featured', 'order'),
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


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'category', 'status', 'is_featured', 'author_name', 'reading_time_minutes', 'published_at')
    list_filter = ('status', 'is_featured', 'category')
    list_editable = ('status', 'is_featured')
    search_fields = ('title_en', 'title_fr', 'title_ar', 'body_en', 'slug', 'tags')
    prepopulated_fields = {'slug': ('title_en',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at', '-created_at')

    fieldsets = (
        (_('Title & Slug'), {
            'fields': ('title_en', 'title_fr', 'title_ar', 'slug'),
        }),
        (_('Excerpt / Summary (Multilingual)'), {
            'fields': ('excerpt_en', 'excerpt_fr', 'excerpt_ar'),
        }),
        (_('Body (Multilingual)'), {
            'fields': ('body_en', 'body_fr', 'body_ar'),
        }),
        (_('SEO Meta (Multilingual)'), {
            'fields': ('meta_title_en', 'meta_title_fr', 'meta_title_ar',
                       'meta_description_en', 'meta_description_fr', 'meta_description_ar',
                       'meta_keywords'),
            'classes': ('collapse',),
        }),
        (_('Taxonomy & Media'), {
            'fields': ('category', 'featured_image', 'featured_image_alt', 'tags'),
        }),
        (_('Author & Reading'), {
            'fields': ('author_name', 'reading_time_minutes'),
        }),
        (_('Publishing'), {
            'fields': ('status', 'is_featured', 'published_at'),
        }),
    )


admin.site.site_header = 'getNexiro Admin'
admin.site.site_title = 'getNexiro Dashboard'
admin.site.index_title = 'Content Management'

