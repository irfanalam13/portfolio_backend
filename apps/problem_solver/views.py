from rest_framework import viewsets, permissions
from .models import Problem, Answer, Tag
from .serializers import ProblemSerializer, AnswerSerializer, TagSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = (
        Problem.objects.select_related("user")
        .prefetch_related("tags", "answers", "answers__user")
        .order_by("-created_at")
    )
    serializer_class = ProblemSerializer
    permission_classes = [permissions.AllowAny]

    lookup_field = "slug"


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.select_related("user", "problem").all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.AllowAny]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer