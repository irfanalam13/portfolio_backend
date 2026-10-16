# apps/projects/filters.py
import django_filters
from .models import Project

class ProjectFilter(django_filters.FilterSet):
    featured = django_filters.BooleanFilter()

    class Meta:
        model = Project
        fields = ["featured"]