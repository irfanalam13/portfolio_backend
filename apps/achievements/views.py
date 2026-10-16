from rest_framework import viewsets
from .models import Achievement, Certification
from .serializers import AchievementSerializer, CertificationSerializer
from apps.core.permissions import IsAdminOrReadOnly


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all().order_by("-date")
    serializer_class = AchievementSerializer
    permission_classes = [IsAdminOrReadOnly]


class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all().order_by("-issue_date")
    serializer_class = CertificationSerializer
    permission_classes = [IsAdminOrReadOnly]
    