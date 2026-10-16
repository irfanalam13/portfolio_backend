from rest_framework import serializers
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
    profile = serializers.SerializerMethodField()
    summary_stats = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()
    navigation = serializers.SerializerMethodField()
    social_links = serializers.SerializerMethodField()

    class Meta:
        model = HomePage
        fields = [
            "id",
            "hero",
            "seo",
            "profile_image",
            "background_images",
            "profile",
            "summary_stats",
            "services",
            "navigation",
            "social_links",
        ]

    def get_background_images(self, obj):
        images = HeroBackground.objects.filter(is_active=True).order_by("order")
        return HeroBackgroundSerializer(images, many=True).data

    def get_profile(self, obj):
        profile = SiteProfile.objects.first()
        return SiteProfileSerializer(profile).data if profile else None

    def get_summary_stats(self, obj):
        return SummaryStatSerializer(SummaryStat.objects.all(), many=True).data

    def get_services(self, obj):
        return ServiceSerializer(Service.objects.filter(is_active=True), many=True).data

    def get_navigation(self, obj):
        return NavigationLinkSerializer(NavigationLink.objects.filter(is_active=True), many=True).data

    def get_social_links(self, obj):
        return SocialLinkSerializer(SocialLink.objects.filter(is_active=True), many=True).data


class SiteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteProfile
        fields = "__all__"


class SummaryStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummaryStat
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class NavigationLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavigationLink
        fields = "__all__"


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = "__all__"
    