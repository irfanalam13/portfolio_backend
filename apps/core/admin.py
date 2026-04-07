from django.contrib import admin
from django.utils.html import format_html
from .models import SEO, HeroImage, HeroContent, HomePage


# 🔥 HERO IMAGE ADMIN (WITH PREVIEW)
@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ["id", "preview", "is_active", "created_at"]
    list_editable = ["is_active"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["image"]
    readonly_fields = ["preview"]

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px; border-radius:5px;" />',
                obj.image.url
            )
        return "-"
    preview.short_description = "Image Preview"


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
                '<img src="{}" style="height:50px; border-radius:5px;" />',
                obj.og_image.url
            )
        return "-"
    preview.short_description = "OG Image"


# 🔥 HOMEPAGE ADMIN (INLINE CONTROL)
@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ["id", "hero", "hero_image", "seo"]
    autocomplete_fields = ["hero", "hero_image", "seo"]