from rest_framework import serializers
from .models import Education
class EducationSerializer(serializers.ModelSerializer):

    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = "__all__"

    def get_logo_url(self, obj):
        return obj.logo.url if obj.logo else None
    