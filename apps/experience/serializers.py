from rest_framework import serializers
from .models import Experience

class ExperienceSerializer(serializers.ModelSerializer):
    company_logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = "__all__"

    def get_company_logo_url(self, obj):
        if not obj.company_logo:
            return None
        url = obj.company_logo.url
        # Cloudinary returns absolute URLs; local ImageField returns a
        # relative path that we expand against the current request host.
        request = self.context.get("request")
        if request and not url.startswith("http"):
            return request.build_absolute_uri(url)
        return url
    