from rest_framework import serializers
from .models import SEO, HeroImage, HeroContent, HomePage


# 🔥 SEO
class SEOSerializer(serializers.ModelSerializer):
    og_image_url = serializers.SerializerMethodField()

    class Meta:
        model = SEO
        fields = "__all__"

    def get_og_image_url(self, obj):
        return obj.og_image.url if obj.og_image else None


# 🔥 HERO IMAGE
class HeroImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HeroImage
        fields = ["id", "image_url", "is_active"]

    def get_image_url(self, obj):
        return obj.image.url


# 🔥 HERO CONTENT
class HeroContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroContent
        fields = "__all__"


# 🔥 HOMEPAGE
class HomePageSerializer(serializers.ModelSerializer):
    hero = HeroContentSerializer()
    seo = SEOSerializer()

    active_hero_images = serializers.SerializerMethodField()

    class Meta:
        model = HomePage
        fields = ["id", "hero", "seo", "active_hero_images"]

    def get_active_hero_images(self, obj):
        images = HeroImage.objects.filter(is_active=True)
        return HeroImageSerializer(images, many=True).data