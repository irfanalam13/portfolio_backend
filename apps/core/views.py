from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import HomePage
from .serializers import (
    HomePageSerializer,
    NavigationLinkSerializer,
    ServiceSerializer,
    SiteProfileSerializer,
    SocialLinkSerializer,
    SummaryStatSerializer,
)
from .models import NavigationLink, Service, SiteProfile, SocialLink, SummaryStat


class HomePageAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        homepage = (
            HomePage.objects
            .select_related("hero", "seo", "profile_image")
            .first()
        )

        if not homepage:
            return Response({
                "hero": None,
                "seo": None,
                "profile_image": None,
                "background_images": [],
                "profile": SiteProfileSerializer(SiteProfile.objects.first()).data if SiteProfile.objects.exists() else None,
                "summary_stats": SummaryStatSerializer(SummaryStat.objects.all(), many=True).data,
                "services": ServiceSerializer(Service.objects.filter(is_active=True), many=True).data,
                "navigation": NavigationLinkSerializer(NavigationLink.objects.filter(is_active=True), many=True).data,
                "social_links": SocialLinkSerializer(SocialLink.objects.filter(is_active=True), many=True).data,
            }, status=status.HTTP_200_OK)

        serializer = HomePageSerializer(homepage)
        return Response(serializer.data, status=status.HTTP_200_OK)