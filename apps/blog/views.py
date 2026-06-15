from rest_framework import viewsets, filters
from .models import Post, Category, Tag
from .serializers import (
    PostSerializer,
    PostCreateUpdateSerializer,
    CategorySerializer,
    TagSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects.filter(is_published=True)
        .select_related("category")
        .prefetch_related("tags")
        .order_by("-created_at")
    )
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PostCreateUpdateSerializer
        return PostSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.query_params.get("category")
        tag = self.request.query_params.get("tag")

        if category:
            queryset = queryset.filter(category__slug=category)

        if tag:
            queryset = queryset.filter(tags__slug=tag)

        return queryset