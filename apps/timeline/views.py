from rest_framework import viewsets
from .models import TimelineEvent
from .serializers import TimelineSerializer
from apps.core.permissions import IsAdminOrReadOnly

class TimelineViewSet(viewsets.ModelViewSet):
    queryset = TimelineEvent.objects.all()
    serializer_class = TimelineSerializer
    permission_classes = [IsAdminOrReadOnly]
    