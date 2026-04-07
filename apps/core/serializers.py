from rest_framework import serializers
from .models import SEO, HeroImage, HeroContent, HomePage


class SEOSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEO
        fields = "__all__"


class HeroImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroImage
        fields = "__all__"


class HeroContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroContent
        fields = "__all__"


class HomePageSerializer(serializers.ModelSerializer):
    hero = HeroContentSerializer()
    seo = SEOSerializer()
    hero_images = serializers.SerializerMethodField()

    class Meta:
        model = HomePage
        fields = ["id", "hero", "seo", "hero_images"]

    def get_hero_images(self, obj):
        images = HeroImage.objects.filter(is_active=True)
        return HeroImageSerializer(images, many=True).data