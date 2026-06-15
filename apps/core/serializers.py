from rest_framework import serializers
from .models import (
    SEO,
    HeroBackground,
    ProfileImage,
    HeroContent,
    HomePage
)


# 🔥 SEO
class SEOSerializer(serializers.ModelSerializer):
    og_image_url = serializers.SerializerMethodField()

    class Meta:
        model = SEO
        fields = "__all__"

    def get_og_image_url(self, obj):
        return obj.og_image.url if obj.og_image else None


# 🔥 HERO BACKGROUND (MULTIPLE)
class HeroBackgroundSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HeroBackground
        fields = ["id", "image_url", "order", "is_active"]

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


# 🔥 PROFILE IMAGE (SINGLE)
class ProfileImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProfileImage
        fields = ["id", "image_url", "is_active"]

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


# 🔥 HERO CONTENT
class HeroContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroContent
        fields = "__all__"


# 🔥 HOMEPAGE (MAIN API)
class HomePageSerializer(serializers.ModelSerializer):
    hero = HeroContentSerializer(read_only=True)
    seo = SEOSerializer(read_only=True)
    profile_image = ProfileImageSerializer(read_only=True)

    background_images = serializers.SerializerMethodField()

    class Meta:
        model = HomePage
        fields = [
            "id",
            "hero",
            "seo",
            "profile_image",
            "background_images",
        ]

    def get_background_images(self, obj):
        images = HeroBackground.objects.filter(is_active=True).order_by("order")
        return HeroBackgroundSerializer(images, many=True).data
    