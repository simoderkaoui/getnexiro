"""
getNexiro — Admin Configuration with Multilingual Support.

Clean, organized admin dashboard for managing EN / FR / AR content.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import (
    SiteConfig, Service, ProjectCategory, Project,
    TeamMember, Testimonial, ClientLogo, Stat, ContactMessage,
)


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Brand Identity'), {
            'fields': ('site_name', 'email', 'phone'),
        }),
        (_('Tagline (Multilingual)'), {
            'fields': ('tagline_en', 'tagline_fr', 'tagline_ar'),
        }),
        (_('Home Hero Headline'), {
            'fields': ('hero_title_en', 'hero_title_fr', 'hero_title_ar'),
        }),
        (_('Home Hero Subtitle'), {
            'fields': ('hero_subtitle_en', 'hero_subtitle_fr', 'hero_subtitle_ar'),
        }),
        (_('About Us Story'), {
            'fields': ('about_text_en', 'about_text_fr', 'about_text_ar'),
        }),
        (_('Mission Statement'), {
            'fields': ('mission_statement_en', 'mission_statement_fr', 'mission_statement_ar'),
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


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'title_fr', 'title_ar', 'icon', 'is_featured', 'order')
    list_filter = ('is_featured', 'icon')
    list_editable = ('is_featured', 'order')
    search_fields = ('title_en', 'title_fr', 'title_ar', 'description_en', 'description_ar')
    ordering = ('order',)

    fieldsets = (
        (_('Titles (Multilingual)'), {
            'fields': ('title_en', 'title_fr', 'title_ar'),
        }),
        (_('Descriptions (Multilingual)'), {
            'fields': ('description_en', 'description_fr', 'description_ar'),
        }),
        (_('Configuration'), {
            'fields': ('icon', 'is_featured', 'order'),
        }),
    )


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_fr', 'name_ar', 'slug')
    prepopulated_fields = {'slug': ('name_en',)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'category', 'is_featured', 'image_preview', 'order')
    list_filter = ('category', 'is_featured')
    list_editable = ('is_featured', 'order')
    search_fields = ('title_en', 'title_fr', 'title_ar', 'description_en')
    ordering = ('order',)

    fieldsets = (
        (_('Titles (Multilingual)'), {
            'fields': ('title_en', 'title_fr', 'title_ar'),
        }),
        (_('Category & Details'), {
            'fields': ('category', 'client_name', 'technologies', 'image'),
        }),
        (_('Descriptions (Multilingual)'), {
            'fields': ('description_en', 'description_fr', 'description_ar'),
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


admin.site.site_header = 'getNexiro Admin'
admin.site.site_title = 'getNexiro Dashboard'
admin.site.index_title = 'Content Management'
