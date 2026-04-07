from rest_framework.viewsets import ModelViewSet
from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    lookup_field = 'slug'