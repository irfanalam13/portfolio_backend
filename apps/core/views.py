from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HomePage
from .serializers import HomePageSerializer


class HomePageAPIView(APIView):
    def get(self, request):
        homepage = HomePage.objects.first()
        serializer = HomePageSerializer(homepage)
        return Response(serializer.data)