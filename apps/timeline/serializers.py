from rest_framework import serializers
from .models import TimelineEvent

class TimelineSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = TimelineEvent
        fields = "__all__"

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None
    