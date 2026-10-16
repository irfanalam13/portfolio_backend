from rest_framework import serializers
from .models import Achievement, Certification


class AchievementSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = "__all__"

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


class CertificationSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Certification
        fields = "__all__"

    def get_image_url(self, obj):
        return obj.image.url if obj.image else (obj.image_url or None)
    