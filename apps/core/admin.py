from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SEO,
    HeroBackground,
    ProfileImage,
    HeroContent,
    HomePage,
    SiteProfile,
    SummaryStat,
    Service,
    NavigationLink,
    SocialLink,
)


# 🔥 HERO BACKGROUND ADMIN (MULTIPLE IMAGES)
@admin.register(HeroBackground)
class HeroBackgroundAdmin(admin.ModelAdmin):
    list_display = ["id", "preview", "order", "is_active", "created_at"]
    list_editable = ["order", "is_active"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["id"]
    readonly_fields = ["preview"]

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px; border-radius:6px;" />',
                obj.image.url
            )
        return "-"
    preview.short_description = "Preview"


# 🔥 PROFILE IMAGE ADMIN (SINGLE IMAGE)
@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):
    list_display = ["id", "preview", "is_active", "created_at"]
    list_editable = ["is_active"]
    list_filter = ["is_active", "created_at"]
    readonly_fields = ["preview"]
    search_fields = ["id", "image"]   # ✅ ADD THIS LINE

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px; border-radius:50%;" />',
                obj.image.url
            )
        return "-"
    preview.short_description = "Profile Preview"


# 🔥 HERO CONTENT ADMIN
@admin.register(HeroContent)
class HeroContentAdmin(admin.ModelAdmin):
    list_display = ["headline", "cta_text", "created_at"]
    search_fields = ["headline", "subheadline", "cta_text"]
    list_filter = ["created_at"]


# 🔥 SEO ADMIN (WITH OG IMAGE PREVIEW)
@admin.register(SEO)
class SEOAdmin(admin.ModelAdmin):
    list_display = ["title", "preview", "created_at"]
    search_fields = ["title", "keywords"]
    readonly_fields = ["preview"]

    def preview(self, obj):
        if obj.og_image:
            return format_html(
                '<img src="{}" style="height:50px; border-radius:6px;" />',
                obj.og_image.url
            )
        return "-"
    preview.short_description = "OG Image"


# 🔥 HOMEPAGE ADMIN (MAIN CONTROL PANEL)
@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ["id", "hero", "profile_image", "seo", "created_at"]
    autocomplete_fields = ["hero", "profile_image", "seo"]


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "title", "location", "availability_status"]


@admin.register(SummaryStat)
class SummaryStatAdmin(admin.ModelAdmin):
    list_display = ["title", "value", "order"]
    list_editable = ["order"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "order", "is_active"]
    list_editable = ["order", "is_active"]
    prepopulated_fields = {"slug": ["title"]}


@admin.register(NavigationLink)
class NavigationLinkAdmin(admin.ModelAdmin):
    list_display = ["label", "href", "order", "is_active"]
    list_editable = ["order", "is_active"]


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "icon", "order", "is_active"]
    list_editable = ["order", "is_active"]

