from rest_framework import viewsets
from .models import TimelineEvent
from .serializers import TimelineSerializer

class TimelineViewSet(viewsets.ModelViewSet):
    queryset = TimelineEvent.objects.all()
    serializer_class = TimelineSerializer
    