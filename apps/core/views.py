from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import HomePage
from .serializers import HomePageSerializer


class HomePageAPIView(APIView):
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
                "background_images": []
            }, status=status.HTTP_200_OK)

        serializer = HomePageSerializer(homepage)
        return Response(serializer.data, status=status.HTTP_200_OK)