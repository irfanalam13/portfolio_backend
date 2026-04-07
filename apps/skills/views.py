from rest_framework import generics
from .models import Skill, SkillCategory
from .serializers import SkillSerializer, SkillCategorySerializer

class SkillListView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class SkillCategoryListView(generics.ListAPIView):
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer