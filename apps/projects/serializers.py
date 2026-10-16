from rest_framework import serializers
from .models import Project





class ProjectSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_thumbnail(self, obj):
        if obj.thumbnail:
            return obj.thumbnail.url
        return obj.thumbnail_url or None