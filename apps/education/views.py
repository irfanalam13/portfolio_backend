from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .selectors import get_all_education
from .serializers import EducationSerializer


class EducationListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = get_all_education()
        serializer = EducationSerializer(queryset, many=True)
        return Response(serializer.data)